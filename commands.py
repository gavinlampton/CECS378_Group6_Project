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
    return_int = return_int.from_bytes(bytes=byte_command, byteorder="big")
    if return_int >= len(Commands):
        return Commands.INVALID
    else:
        return Commands(return_int)


def str_to_command(input_str):
    # https://www.pythonpool.com/check-data-type-python/
    # Got the isInstance function from here.
    if isinstance(input_str, bytes):
        return from_byte(input_str)
    try:

        for commands in Commands:
            # https://www.geeksforgeeks.org/case-insensitive-string-comparison-in-python/
            # idea for the case-insensitive comparison
            if input_str.lower() == commands.name.lower():
                return Commands(commands.value)
    except ValueError:
        return Commands.INVALID


# https://www.geeksforgeeks.org/enum-in-python/
# created using this tutorial
class Commands(Enum):
    REQUEST = 1
    FILENAME = 2
    FILE = 3
    END_TRANSFER = 4
    INVALID = 5


print(from_byte(to_byte(Commands.REQUEST)).name)

