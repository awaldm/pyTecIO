![example workflow]([https://github.com/github/docs/actions/workflows/main.yml/badge.svg](https://github.com/awaldm/pyTecIO/actions/workflows/pytecio.yml/badge.svg))
[![License: MIT]([https://img.shields.io/badge/License-MIT-yellow.svg](https://img.shields.io/github/license/awaldm/pytecio
))](https://opensource.org/licenses/MIT)

# pytecio
python reader for unstructured Tecplot ASCII data

## Purpose
This is my old Tecplot data reader. The original purpose was to have a reader routine that does not make too many assumptions about 
the structure of the Tecplot data file - for instance, it does not matter to Tecplot whether the variables are all listed in the same
line or below the "ZONE T" keyword. It turns out that Tecplot itself is rather liberal when parsing such data, which is what I aimed to replicate.

## Installation
Clone the repo and install via `pip install .`

## Usage
### Unstructured ASCII data
Tecplot unstructured data consists of nodal data and element connectivity information. Supply the Tecplot file name to the function:
```
from pytecio import *
zones, dfs, elements = read_ascii(filename, verbose=0)
```
  * `zones` returns a list of the zone names
  * `dfs` returns a list of pandas dataframes, where each dataframe is the (nodal) data contained in the Tecplot zone
  * `elements` returns a list of pandas dataframes containing the Tecplot connectivity list

`list(dfs[0])` returns a list of the variable names 



## Status
The repo was renamed from read_tecplot to pytecio to better reflect what it does

## Requirements
* numpy (tested with 1.12.0)
* pandas (tested with 0.19.1)

## Known issues
* Assumes all-uppercase Tecplot keywords (i.e. "ZONE T = ", does not recognize "Zone T = ")
* Ignores the AUXDATA
