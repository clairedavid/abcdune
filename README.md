# ABC DUNE

## Purpose
Python script to convert the DUNE TDR glossary from LaTeX to HTML.
The automatically created webpage has all DUNE words listed, with cross-references done via HTML links. A horizontal menu with all letters of the alphabet allows for a quick access.

Demo [here](http://davidc.web.cern.ch/davidc/abcdune/).

## Script
```sh
python3 convert_glossary_tex_to_html.py [-h] [infile]
```
- The script takes as argument the LaTeX glossary filename. If none is given, it attempts to read "glossary.tex" 
- Tested with [glossary.tex](https://github.com/DUNE/dune-tdr/blob/master/common/glossary.tex) (last edit: January 27, 2020)

## Status
- Done with Python3.
- The content is temporarily hosted on my CERN account for a demo.
- Need some clean-up of remaining LaTeX commands (equations, SI{}{} commands, etc)
