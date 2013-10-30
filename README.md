### Regular Expressions for Python ###
*Jordan Degner
*30 October 2013

A Python module for CSCE 428 (Automata, Computation, and Formal Languages) that, given a newline-delimited text file of the form:

< regular expression >
< strings >

Will evaluate all of the provided strings for a match against the provided regular expression.

## Running the Program ##
To run this program, execute the command `regexp.py < <inputfile>` from the command line. Or, if you prefer, simply
provide a pattern and expressions from standard input.

## Input ##
This module takes one input file from the command line and parses its first line as a regular expression and its remaining
lines as strings to be evaluated for membership in this regular expression's language.

## Output ##
After operating on the provided input and determining which strings are a member of the regular expression's language,
this module will print each string's membership status to the command line.

## The Regular Expression ##
The provided regular expression must contain only the characters 'a', 'b', 'e' (the empty string), '|' (the union operator), 
'*' (the Kleen closure), '(', and ')'. It must also be of at most 80 characters. This assignment assumes the integrity of the 
provided regular expression and does not attempt to validate it before performing comparisons.

## How It Works ##
1) The provided regular expression is parsed into a non-deterministic finite automaton.
2) All remaining lines are saved into a list of strings.
2) Every string in the list is tested against this automaton, and as they pass or fail, the results will be reported to standard
output.

## Technologies Used ##
- Python 2.7.5