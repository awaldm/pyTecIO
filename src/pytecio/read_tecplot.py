"""Readers for Tecplot ASCII files."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

# We rely on regex quite a lot, so make it a bit more structured with those
VARIABLE_RE = re.compile(r'"([^"]*)"')
ZONE_NAME_RE = re.compile(r'zone\s+t\s*=\s*"([^"]*)"', re.IGNORECASE)
NODES_RE = re.compile(r'\bnodes\s*=\s*(\d+)', re.IGNORECASE)
ELEMENTS_RE = re.compile(r'\belements\s*=\s*(\d+)', re.IGNORECASE)
DATASETAUX_RE = re.compile(r'^\s*datasetaux', re.IGNORECASE)


def parse_vars(vars_in):
    """Normalize raw Tecplot variable names (remove quotes basically)."""
    variables = [item.strip() for item in vars_in]
    return [item.replace("'", "").replace('"', "") for item in variables]


def is_number(value):
    """Return True when *value* can be interpreted as a number."""
    try:
        float(value)
        return True
    except ValueError:
        pass

    try:
        unicodedata.numeric(value)
        return True
    except (TypeError, ValueError):
        pass

    return False


def _extract_variables(line):
    """Extract quoted variable names from a Tecplot header line via regex."""
    return VARIABLE_RE.findall(line)


def _parse_zone_name(line):
    """Extract a zone name from a ZONE header line via regex."""
    match = ZONE_NAME_RE.search(line)
    if match:
        return match.group(1).strip()
    return line.strip()


def _extract_int(pattern, line):
    """Extract an integer metadata value from a Tecplot header line via regex."""
    match = pattern.search(line)
    if match:
        return int(match.group(1))
    return None


def _to_numeric_frame(rows, columns):
    """Build a numeric DataFrame with normalized column names from lists."""
    frame = pd.DataFrame(rows, columns=parse_vars(columns))
    return frame.apply(pd.to_numeric)


def _consume_zone_row(fields, data, elems, variables, dfs, els, struct, nodes, elements):
    """Append a data or connectivity row to the active zone."""
    if struct or nodes is None or len(data) < nodes:
        data.append(fields)
        if not struct and nodes is not None and len(data) == nodes:
            dfs.append(_to_numeric_frame(data, variables))
        return

    if elements is None or len(elems) >= elements:
        return

    elems.append(fields)
    if len(elems) == elements:
        els.append(pd.DataFrame(elems).apply(pd.to_numeric))


def read1D(tecplotFileName, verbose=0, to_pandas=False):
    """Read Tecplot list-like (1D) data."""
    tpfile_path = Path(tecplotFileName)
    with tpfile_path.open("r", encoding="utf-8") as tpfile:
        lines = tpfile.readlines()

    variables = []
    header_lines = 0
    max_feasible_header = min(30, len(lines))

    for index, line in enumerate(lines[:max_feasible_header]):
        upper_line = line.upper()

        if "VARIABLES" in upper_line:
            variables = _extract_variables(line)
            if verbose:
                print(f"Variables on line {index}: {variables}")
            header_lines = index + 1

        if "TITLE" in upper_line:
            if verbose:
                print(f"Title on line {index}: {line.strip()}")
            header_lines = index + 1

        if "ZONE" in upper_line:
            if verbose:
                print(f"Zone on line {index}: {line.strip()}")
            header_lines = index + 1

        if "DT" in upper_line:
            if verbose:
                print(f"DT on line {index}: {line.strip()}")
            header_lines = index + 1

    if not variables:
        raise ValueError(f"No VARIABLES header found in {tpfile_path}")

    if verbose:
        print(f"Found {header_lines} header lines.")

    data = np.loadtxt(tpfile_path, skiprows=header_lines)

    if verbose:
        print(f"{len(lines)} lines read.")

    if to_pandas:
        return pd.DataFrame(data, columns=parse_vars(variables))
    return parse_vars(variables), data


def read_ascii(filename, verbose=0):
    """Read general Tecplot ASCII data into pandas DataFrames."""
    file_path = Path(filename)

    struct = True
    variables = []
    zones = []
    mode = 0
    dfs = []
    els = []
    data = []
    elems = []
    nodes = None
    elements = None

    with file_path.open("r", encoding="utf-8") as datafile:
        for line in datafile:
            stripped = line.strip()
            upper_line = line.upper()

            if not stripped or stripped.startswith("#"):
                continue

            if "TITLE" in upper_line:
                if verbose:
                    print(f"Title: {stripped}")
                mode = 0
                continue

            if "VARIABLES" in upper_line:
                variables = _extract_variables(line)
                if verbose:
                    print(f"Variables: {variables}")
                mode = 1
                continue

            if "ZONE T" in upper_line:
                if mode == 3 and struct and data:
                    dfs.append(_to_numeric_frame(data, variables))

                zone_name = _parse_zone_name(line)
                nodes = _extract_int(NODES_RE, line)
                elements = _extract_int(ELEMENTS_RE, line)
                struct = nodes is None
                data = []
                elems = []

                zones.append(zone_name)
                if verbose:
                    print(f"Zone: {zone_name}")
                mode = 2
                continue

            nodes_value = _extract_int(NODES_RE, line)
            if nodes_value is not None:
                nodes = nodes_value
                struct = False
                if verbose:
                    print(f"Nodes: {nodes}")

            elements_value = _extract_int(ELEMENTS_RE, line)
            if elements_value is not None:
                elements = elements_value
                if verbose:
                    print(f"Elements: {elements}")

            if "DT=(" in upper_line:
                if verbose:
                    print(f"DT line: {stripped}")
                mode = 3
                continue

            if "STRANDID" in upper_line or "DATAPACKING" in upper_line:
                continue

            if mode == 1:
                if DATASETAUX_RE.match(line):
                    continue
                variables.extend(_extract_variables(line))
                continue

            fields = stripped.split()
            if mode == 2 and fields and is_number(fields[0]):
                mode = 3

            if mode == 3 and fields:
                _consume_zone_row(fields, data, elems, variables, dfs, els, struct, nodes, elements)

    if mode == 3 and struct and data:
        dfs.append(_to_numeric_frame(data, variables))

    if verbose:
        print(zones)

    return zones, dfs, els
