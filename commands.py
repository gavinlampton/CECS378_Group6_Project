from enum import Enum
from sys import getsizeof


def to_byte(command):
    command_int = command.value
    # https://theprogrammingexpert.com/python-int-to-bytes/
    # int to byte
    # https://codeblessu.com/python/size-of-data-types.html
    # getsizeof
    return command_int.to_bytes(getsizeof(command_int), byteorder="big")


def from_byte(byte_command):
    return_int = 0
    # https://theprogrammingexpert.com/python-int-to-bytes/
    # bytes to int.
    return Commands(return_int.from_bytes(bytes=byte_command, byteorder="big"))

def str_to_command(input_str):
    for commands in Commands:
        # https://www.geeksforgeeks.org/case-insensitive-string-comparison-in-python/
        # idea for the case-insensitive comparison
        if input_str.lower() == commands.name.lower():
            return Commands(commands.value)


# https://www.geeksforgeeks.org/enum-in-python/
# created using this tutorial
class Commands(Enum):
    REQUEST = 1
    FILENAME = 2
    FILE = 3
    END_TRANSFER = 4


print(from_byte(to_byte(Commands.REQUEST)).name)

