#!/bin/python3
from os import execv
from sys import argv
from random import randint
print("Have a random number: ")
print(randint(0, 10000))
execv(argv[0], argv)
