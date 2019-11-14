#PSRCATPY
#########################################
A very simple python package that finds all sources within a certain radius of a position.

It expects psrcat to be installed and on $PATH of the system

Provides a nice wrapper around the psrcat queries and returns a JSON string of all parameters that we asked for

Requirements:

Works on python 3.7

Needs Astropy > 3.2.3

Jinja2

Installation:

Via pip:

`pip install psrcatpy`

Usage:

example usage:

import psrcatpy

psr = psrcatpy.PsrCat("JNAME P0 DM RAJ DECJ S1400","03:29:54.2", "+54:52:56", 10.0, 5.0, 10.0)

json = psr.run_query()

#########################################
