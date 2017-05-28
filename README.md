# read_tecplot
python reader for unstructured Tecplot ASCII data

## Introduction
This is my old Tecplot data reader. The original purpose was to have a reader routine that does not make too many assumptions about 
the structure of the Tecplot data file - for instance, it does not matter to Tecplot whether the variables are all listed in the same
line or below the "ZONE T" keyword. It turns out that Tecplot itself is rather liberal when parsing such data, which is what I aimed to replicate.


## Usage
Supply the Tecplot file name to the function:
```
zones, dfs, elements = read_tecplot(filename, verbose=0)
```
  * `zones` returns a list of the zone names
  * `dfs` returns a list of pandas dataframes, where each dataframe is the (nodal) data contained in the Tecplot zone
  * `elements` returns a list of pandas dataframes containing the Tecplot connectivity list

`list(dfs[0])` returns a list of the variable names 

## Requirements
* numpy (tested with 1.12.0)
* pandas (tested with 0.19.1)

## Known issues
* Assumes all-uppercase Tecplot keywords (i.e. "ZONE T = ", does not recognize "Zone T = ")
* Ignores the AUXDATA
* Presently does not handle structured data anymore
