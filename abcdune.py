#!/usr/local/bin/python3

# ##########################################################
# 
# Script to convert the DUNE LaTeX glossary into HTML
#
# Glossary:      
# https://github.com/DUNE/dune-tdr/blob/master/common/glossary.tex
#
# Author:        Claire David    cdavid@fnal.gov
# Date created:  February 24, 2020
# Status:        dev
#          
# ##########################################################
import os
import sys
import re
import argparse
import json
import string

def replace_percent_in_html_code(line):
    
    """
    escaped percent replaced by HTML code
    """
    line = line.replace("\%", "&percnt;")
    return(line)

def remove_comment(line):
    
    """
        removing all LaTeX comments (full line or end of line)
    """
    if "%" not in line:
        return(line.rstrip())
    else:
        index_percentage = line.index("%")
        line_with_no_comment = line[:index_percentage]
        return(line_with_no_comment.rstrip())

def gls_to_html_link(defString, gls_tag_type, DUNEdict):

    # the defString may contain gls{} or glspl{} tags to be replaced
    # by HTML <a></a> tags

    isPlural = True if gls_tag_type is "glspl" else False

    re_gls  = re.compile(r'\\' + gls_tag_type + '\{(.*?)\}')
    glsTags = re_gls.findall(defString)

    for glsTag in glsTags:
        
        tagToReplace = "\\" + gls_tag_type + "{" + glsTag + "}"
        
        # The link text in HTML is either:
        # "term" entry in dictionary if type 'word'
        # "abbrev" entry (acronym) if type 'abbrev'

        link_text = DUNEdict[glsTag]["term"] if DUNEdict[glsTag]["type"] is "word" else DUNEdict[glsTag]["abbrev"]
        if isPlural:
            link_text = link_text + "s"

        defString  = defString.replace(tagToReplace, "<a href=\"#" + glsTag + "\">" + link_text + "</a>")
    
    return defString 


def latex_into_html(defLaTeX, DUNEdict):

    # Replace \gls{} and \glspl{} tags with HTML <a></a> link tags
    stringHTML = gls_to_html_link(defLaTeX, "gls", DUNEdict)
    stringHTML = gls_to_html_link(stringHTML, "glspl", DUNEdict)
    stringHTML = stringHTML.replace("  ", " ")
    
    # Replace the newcommand{} from defs.tex by the proper latex

    # pypandoc to resolve all remaining latex-to-html issues:
    
    return stringHTML.rstrip(' ') + "." # adding period at the end of the HTML definition 

def main():

    parser = argparse.ArgumentParser(description='Store all DUNE words and acronyms from the LaTeX glossary into a JSON file and HTML index.')
    #parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), help='Name of glossary tex file.' )
    #parser.add_argument('-i', type=argparse.FileType('r'), help='Name of glossary tex file.', dest="src")
    #parser.add_argument('-o', type=argparse.FileType('w'), help='Name of glossary html file.', dest="dest")
    parser.add_argument('-i', help='Path to glossary tex file.',  dest="src")
    parser.add_argument('-d', help='Path to definition tex file.',dest="defs")
    parser.add_argument('-o', help='Path to glossary html file.', dest="dest")
    args = parser.parse_args()
     
    #filename = args.infile
    print(args.src)

    print(args.dest)
    
     
    #else:
    #    print("No argument given, opening default file 'glossary.tex'")
    #    filename = 'glossary.tex'

    """ 
    try: 
        with open(args.src, 'r') as f:
            content = f.readlines()
    finally: f.close()
    """
    #------------------------
    # Opening defs.tex
    #------------------------
    f = open(args.defs)
    try:
        defs_content = f.readlines()
    except: pass
    finally: f.close()

    # STEP 1: the escaped LaTeX percent is replaced with its HTML code
    defs_content_percntHTML = [ replace_percent_in_html_code(line) for line in defs_content if "\\newcommand{" in line]

    # STEP 2: now removing LaTeX comments
    defs_no_comment = [ remove_comment(line) for line in defs_content_percntHTML ]

    # STEP 3: fill list of \newcommand items:
    one_line_defs = "".join(defs_no_comment)
    one_line_defs = one_line_defs.replace("\n","")
    list_defs     = one_line_defs.split("\\newcommand{")
    
    # STEP 4: storing \newcommands in dictionary
    # Example 1:
    # \newcommand{\threed}{3D\xspace}
    # defs_dict["\threed"] = { N_args: 0, def_latex: "3D\xspace" }
    # Example 2:
    # \newcommand{\bigo}[1]{\ensuremath{\mathcal{O}(#1)}}
    # defs_dict["\bigo"] = { N_args: 1 , def_latex: "\ensuremath{\mathcal{O}(#1)}" }

    defs_dict = {} 
    for line in list_defs:
        if "}[" in line:
            def_command , sep , Nargs_and_def_latex = line.partition("}[")
            N_args_str , sep , def_latex = Nargs_and_def_latex.partition("]{")
            N_args = int(N_args_str)
            
        else:
            def_command , sep, def_latex  = line.partition("}{")
            N_args = 0

        def_latex = def_latex[:-1] if def_latex.endswith('}') else def_latex
        def_latex = def_latex.replace('\\xspace', ' ')

        defs_dict[def_command] = { "N_args": N_args, "def_latex": def_latex }

    for key , info in defs_dict.items():
        print("%s\t\t%d\t\t%s"%(key,info["N_args"], info["def_latex"]))

    print(len(defs_dict))
    sys.exit(2)

    #------------------------
    # Opening glossary.tex
    #------------------------
    f = open(args.src)
    try: 
        content = f.readlines()
    except: pass
    finally: f.close()    

    # STEP 1: the escaped LaTeX percent is replaced with its HTML code
    content_percntHTML = [ replace_percent_in_html_code(line) for line in content]

    # STEP 2: now removing LaTeX comments
    content_no_comment = [ remove_comment(line) for line in content_percntHTML if "\\newcommand" not in line]

    # STEP 3: fill list of "\\new" LaTeX items: [command|duneword|duneabbrev|duneabbrevs]
    one_line_glossary = "".join(content_no_comment)
    one_line_glossary = one_line_glossary.replace("\n","")
    one_line_glossary = one_line_glossary.replace("} {", "}{")
    list_glossary = one_line_glossary.split("\\new")

    # STEP 4: storing all DUNE words in dictionary into format:
    #__________________________________________________________________
    #
    #                 label     | abbrev |  term  |  terms | description
    #__________________________________________________________________
    # LaTeX args:  
    # newduneword      [1]      |        |   [2]  |        |   [3]   
    # newduneabbrev    [1]      |  [2]   |   [3]  |        |   [4]
    # newduneabbrevs   [1]      |  [2]   |   [3]  |   [4]  |   [5]
    #__________________________________________________________________
    # 
    # dic = [ key, [type, abbrev, term, terms , defLaTeX, defHTML ] ]
    #__________________________________________________________________
    #
    # Note: the separator for the first tags is "}{" but it is present 
    # in custom LaTeX commands inside the description
    # Parsing thus using partition("}{")

    DUNEdict = {}

    for line in list_glossary:

        if line.startswith( 'duneword{' ):
            
            # duneword{key}{term}{ description }
            
            key , sep,  info       = line[9:].partition("}{")
            term, sep, description = info.partition("}{") 
            description            = description[:-1] if description.endswith('}') else description
            defLaTeX               = description
            DUNEdict[key]          = {"type": "word", "term": term, "defLaTeX": defLaTeX}

        elif line.startswith( 'duneabbrev{' ):
    
            # duneabbrev{key}{abbrev}{term}{ description }

            key , sep, info1       = line[11:].partition("}{")
            abbrev, s, info2       = info1.partition("}{")
            term ,  s, description = info2.partition("}{")
            defLaTeX               = description[:-1] if description.endswith('}') else description
            DUNEdict[key]          = {"type": "abbrev", "abbrev": abbrev, "term": term, "defLaTeX": defLaTeX}

        elif line.startswith( 'duneabbrevs{' ):
    
            # duneabbrevs{key}{abbrev}{term}{terms}{ description }

            key , sep, info1       = line[12:].partition("}{")
            abbrev, s, info2       = info1.partition("}{")
            term ,  s, info3       = info2.partition("}{")
            terms,  s, description = info3.partition("}{")
            defLaTeX               = description[:-1] if description.endswith('}') else description
            DUNEdict[key]          = {"type": "abbrevs", "abbrev": abbrev, "term": term, "terms": terms, "defLaTeX": defLaTeX}
    
        else:
            continue 

    #===== Description in HTML =====
    # Need to have loaded full dictionnary to convert
    # the referenced acronyms into html links

    for key , info in DUNEdict.items():

        defHTML = latex_into_html(info["defLaTeX"], DUNEdict)
        info["defHTML"] = defHTML

    #===== Export in JSON file =====
    
    jsonfile = 'DUNE_words.json'
    with open(jsonfile, 'w') as fp:
        json.dump(DUNEdict, fp, indent=4, sort_keys=True)
    print("DUNE words exported in JSON file " + jsonfile)

    #===== Write HTML content =====
    content = r'''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
    <link rel="stylesheet" media="screen" type="text/css" title="Design" href="css/abcdune.css">
  <title>A B C DUNE</title>
</head>
<body>
<div id="content">

<center>
<img src="gfx/abcdune_logo.png" alt="A B C DUNE" id="header">
<h2>Speak neutrinos</h2>

<p class="alphabet_menu">
'''

    # Letters of alphabet as horizontal menu:
    abc = list(string.ascii_uppercase)
    abc.append("&num;")

    for letter in abc:
        content += '<a href="#' + letter + '">' + letter + '</a>\n'
    content += r'''</p>
</center>
'''
    #==== Loop over alphabet =====
    print("Writing HTML index file...")

    currentLetter = "DUMMY"
    doHeader = True

    for letter in abc:

        content += '<h1 id="'+ letter +'">'+ letter +'</h1>\n<dl>\n'
        
        for key, info in sorted(DUNEdict.items()):

            if key.startswith(letter.lower()) or (letter is "&num;" and key[0].isdigit()):

                # Format the term if referenced word (gls)
                termHTML = gls_to_html_link(info["term"], "gls", DUNEdict)

                if info["type"] is not "word": # cases abbrev and abbrevs

                    content += '  <dt id = "' + key + '">' + info["abbrev"] + '</dt>\n'
                    content += '  <dd>' + termHTML + '<br>'
                else:
                    content += '  <dt id = "' + key + '">' + termHTML + '</dt>\n'
                    content += '  <dd>'
                content += info["defHTML"] + '</dd>\n'
        # end of letter block
        content += '</dl>\n'
    # end of HTML:
    content += '<br>\n</div>\n</body>\n</html>'

    #===== Export in HTML index =====
    f_html = open(args.dest, 'w')
    f_html.write(content)
    print("HTML file created in:  " + args.dest )

    """
    f_html = "./docs/index.html"
    with open(f_html,'w') as f:
        f.write(content)
    print("HTML file created in:  " + f_html)
    """


if __name__ == '__main__':
    
    main()
