# ABC DUNE

## Purpose
Python script to convert the DUNE TDR glossary from LaTeX to HTML.
The automatically created webpage has all DUNE words listed, with cross-references done via HTML links. A horizontal menu with all letters of the alphabet allows for a quick access.

Demo [here](https://clairedavid.github.io/abcdune/).

## Script
```sh
python3 abcdune.py -i glossary.tex -d defs.tex -o docs/index.html
```
- The script takes as arguments the LaTeX glossary and defition (custom commands) filenames. 
<!--- Tested with [glossary.tex](https://github.com/DUNE/dune-tdr/blob/master/common/glossary.tex) (last edit: May 7, 2020) ---> 

## Status
- Done with Python3.
- Currently cleaning source file with coherent self-referencing (gls tags)
- Soon: calling python pandoc for converting LaTeX formulae/commands into HTML codes
