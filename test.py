#!/bin/python3
import os;
import sys;
import random;
print("Have a random number: ")
print(random.randint(0,10000))
os.execv(sys.argv[0], sys.argv)

