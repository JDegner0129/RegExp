### Regular Expressions for Python ###

A Python module for CSCE 428 (Automata, Computation, and Formal Languages) that, given a newline-delimited text file of the form:

[ regular expression ]
[ strings ]

Will evaluate all of the provided strings for a match against the provided regular expression.

## Running the Program ##
To run this program, download the source from this repository, and run `python regexp.py <inputfile>`.

## Input ##
This module takes one input file from the command line and parses its first line as a regular expression and its remaining
lines as strings to be evaluated for membership in this regular expression's language.

## Output ##
After operating on the provided input and determining which strings are a member of the regular expression's language,
this module will print each string and its membership status to the command line.

## The Regular Expression ##
The provided regular expression must contain only the characters 'a', 'b', 'e' (the empty string), '|' (the union operator), 
'\*' (the Kleen closure), '(', and ')'. It must also be of at most 80 characters. This assignment assumes the integrity of the 
provided regular expression and does not attempt to validate it before performing comparisons.

## How It Works (WIP) ##
1) The provided regular expression is parsed into a parse tree-like structure.
2) All remaining lines are saved into a list of strings.
2) Every string in the list is parsed against this parse tree, and an index is maintained of the passing and failing strings.
3) Once all strings have been parsed, they are printed along with their status, line-by-line.

## Technologies Used ##
- Python 2.7.5
