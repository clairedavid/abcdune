# ABC DUNE

## Purpose
Python script to convert the DUNE TDR glossary from LaTeX to HTML.
The automatically created webpage has all DUNE words listed, with cross-references done via HTML links. A horizontal menu with all letters of the alphabet allows for a quick access.

Demo [here](https://clairedavid.github.io/abcdune/).

## Script
```sh
python3 abcdune.py -i glossary.tex -d defs.tex -o docs/index.html
```
- The script takes as arguments the LaTeX glossary and definitions (custom commands) filenames. 
<!--- Tested with [glossary.tex](https://github.com/DUNE/dune-tdr/blob/master/common/glossary.tex) (last edit: May 7, 2020) ---> 

## Updates
- More information on how to request a new acronym or correct one can be found in the associated wiki page [here](https://wiki.dunescience.org/wiki/ABC_DUNE).
