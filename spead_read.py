#!/usr/bin/env python3

with open('material.txt', 'r') as file:
    the_lines = [i for i in file.read().split('\n') in len(i) != 0]

the_line = the_lines[0].split(' ')  # puts each word as list item in "the_line"
' '.join(the_line[0:5])  # prints 5 words of the line, space separated
