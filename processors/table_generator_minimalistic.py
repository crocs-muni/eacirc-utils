#!/usr/bin/python3

from __future__ import division

import argparse
import sys
import json # for storing the results

class Result:
    def __init__(self, fun_name, rounds, rej, total):
        self.fun_name = fun_name
        self.rounds = rounds
        self.rej = rej
        self.total = total
    def __init__(self, **entries):
        self.__dict__.update(entries)

results = []

crit_val = 0.01
max_cells = 10

header = r"""
\documentclass[twoside,a4paper]{article}

% ===== LOADING PACKAGES =====
% language settings, main documnet language last
\usepackage[english]{babel}
% enabling new fonts support (nicer)
\usepackage{lmodern}
% setting input encoding
\usepackage[utf8]{inputenc}
% setting output encoding
\usepackage[T1]{fontenc}
% math symbols and environments
\usepackage{mathtools}
% packages for complex tables
\usepackage{tabularx}
\usepackage{multirow}
\usepackage{float}

\usepackage[top=3.0cm, bottom=3cm, left=3cm, right=3cm]{geometry} % pc version
% package to make bullet list nicer
\usepackage{enumitem}
\setitemize{noitemsep,topsep=3pt,parsep=3pt,partopsep=3pt}

\usepackage[table]{xcolor}

\begin{document}

\newcommand{\fd}{\cellcolor{red!13}}
\newcommand{\fn}{\cellcolor{green!13}}

\begin{table}[H]
\centering
\label{res_usable}
\begin{tabular}{l|l l l l l l l l l l l}
Function\textbackslash{}rounds & 0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10\\ \hline
"""

footer = r"""
\end{tabular}
\caption{Usable testbed results}
\end{table}

\end{document}
"""

def print_tex_table(results, of):
    prev = None
    p_rounds = max_cells

    of.write(header)
    of.write(r'rnd\_rnd     & \fn{}')
    of.write(str(crit_val))
    of.write(r' & --    & --    & --    & --    & --    & --    & --    & --    & --    & --   \\')
    
    for res in results:
        if res['rounds'] > max_cells:
            p_rounds = res['rounds']
            continue

        if res['fun_name'] != prev:
            prev = res['fun_name']
            # finish last cells of prev line (pad nonmeasured results with 'passed' mark)
            for i in range(p_rounds, max_cells):
                of.write(r' & \fn{}' + '--'.ljust(5))
            of.write(r'\\')
            of.write('\n')
            # new line and new function name
            if res['fun_name'] == 'rnd_rnd':
                of.write(r'rnd\_rnd'.ljust(12))
            else:
                of.write(res['fun_name'].ljust(12))
            # pad nonmeasured results with 'failed' mark
            for i in range(0, res['rounds']):
                of.write(r' & \fd{}' + '--'.ljust(5))
        # write current results
        if res['rej'] / res['total'] > 2*crit_val:
            of.write(r' & \fd{}' + str(res['rej'] / res['total']).ljust(5))
        else:
            of.write(r' & \fn{}' + str(res['rej'] / res['total']).ljust(5))
        p_rounds = res['rounds']

    # finish last cells of prev line (pad nonmeasured results with 'passed' mark)
    for i in range(p_rounds, max_cells):
        of.write(r' & \fn{}' + '--'.ljust(5))

    of.write(footer)


if __name__ == "__main__":
    # arg parser
    parser = argparse.ArgumentParser(description='Process EACirc results output by postprocessor.py.',
        epilog='Opens json file and generates tables for presentation.')
    parser.add_argument('-i', '--in', dest='inf', type=str, help='path to file res.json from postprocessor.py')
    parser.add_argument('-o', '--out', dest='outf', type=str, help='output path')
    parser.add_argument('-c', '--criticalValue', dest='crit', type=float, default=crit_val, help='output path')

    if len(sys.argv) < 2:
        sys.argv.append("-h")
        args = parser.parse_args()
        exit(1)

    args = parser.parse_args()

    crit_val = args.crit

    with open(args.inf, 'r') as res:
        results = json.load(res)

    with open(args.outf, 'w') as of:
        print_tex_table(results, of)
        
    exit(0)
