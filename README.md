![CI](https://github.com/awaldm/pyTecIO/actions/workflows/pytecio.yml/badge.svg)
![License: MIT](https://img.shields.io/github/license/awaldm/pytecio)

# pytecio

`pytecio` is a small reader for Tecplot ASCII files.

This gives you a lightweight way to pull the data into Python and move on.

## Scope

`pytecio` is intentionally limited.

- Reads legacy Tecplot ASCII data.
- Returns numeric `pandas.DataFrame` objects for zone data.
- Returns numeric connectivity tables for simple unstructured zones.
- Works without Tecplot or a Tecplot license.

It is not intended to be a full Tecplot API replacement.

## What Is Supported

The current test suite covers:

- Structured ASCII zones.
- Simple unstructured ASCII zones with `Nodes=` and `Elements=`.
- Variable definitions on one line or split across multiple lines.
- Lowercase or uppercase Tecplot keywords.
- Multi-zone files.
- 1D/list-style Tecplot monitor files via `read1D()`.

## What Is Not Supported

- Binary Tecplot files such as `.plt` or `.szplt`.
- Full Tecplot feature coverage.
- Preserving `AUXDATA` metadata.
- Rich mesh semantics beyond the raw connectivity table.

Quoted variable names are the tested path.

## Installation

Install from a clone:

```bash
pip install .
```

Dependencies:

- `numpy`
- `pandas`

I recommend using `uv`, even though this is not a fully uv managed repo. So instead of `uv sync`:

```bash
uv venv
uv pip install -e ".[test]"
uv run pytest -q
```

## Usage

Read a Tecplot ASCII file:

```python
from pytecio import read_ascii

zones, zone_data, connectivity = read_ascii("solution.dat")
```

Returned values:

- `zones`: list of zone names as plain strings.
- `zone_data`: list of numeric `pandas.DataFrame` objects, one per zone.
- `connectivity`: list of numeric `pandas.DataFrame` objects for unstructured connectivity.

Read a Tecplot-style 1D monitor file:

```python
from pytecio import read1D

monitor = read1D("monitor.dat", to_pandas=True)
```

`read1D(..., to_pandas=True)` returns a numeric `pandas.DataFrame`. Without `to_pandas=True`, it returns `(variables, data)` where `data` is a NumPy array.

## Development

Run the tests with:

```bash
pip install -e ".[test]"
pytest -q
```

The repository includes small Tecplot ASCII fixtures for structured, unstructured, and multi-zone cases under `tests/testdata/`.
