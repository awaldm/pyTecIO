"""Public package API for pytecio."""

from .read_tecplot import read1D, read_ascii

read_1d = read1D

__all__ = ["read1D", "read_1d", "read_ascii"]
