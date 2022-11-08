#!/usr/bin/env python3

from os import system, name as os_name
from time import sleep


def clear():
    '''Clears the screen depending on the os name'''
    if os_name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


the_text = 'material.txt'
with open(the_text, 'r') as file:
    the_lines = [i for i in file.read().split('\n') if len(i) != 0]

the_line = the_lines[0].split(' ')  # puts each word as list item in "the_line"
' '.join(the_line[0:5])  # prints 5 words of the line, space separated

first_word = 0
last_word = 2
sleep_time = 0.3
while True:
    if last_word >= 400:
        break
    print(' '.join(the_line[first_word:last_word]))
    sleep(sleep_time)
    clear()
    first_word += 2
    last_word += 2



def main():
    '''The Main Event'''


main