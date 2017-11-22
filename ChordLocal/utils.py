#!/usr/bin/env python3

"""
    utils.py - Contains helper functions.
    Author:
        - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
        - Hoanh An (hoanhan@bennington.edu)
    Date: 10/30/2017
"""

import hashlib
from const import m

def chord_hash(input_string):
    """
    Use SHA-1 hash to hash a string, convert it to integer and shift right (160 - m) places

    Why shifting right (160 - m) places:
        - Shifting right m places equals to dividing 2^m.
        - Given m and a value 2^160, in order to find 2^m, need to need to divide 2^160 by 2^(160-m)

    :param input_string: String
    :return: String
    """
    h = hashlib.sha1()  # 160 bit string
    encoded_data = input_string.encode('utf-8')
    h.update(encoded_data)
    hex_string = h.hexdigest()
    hex_value = int(hex_string, 16)
    hash_integer_value = hex_value >> (160 - m)
    return hash_integer_value

def constrain(value):
    """
    Returns a value modulo 2^m. Used to wrap the value between 0 and 2^m.
    :param value: Int
    :return: Int
    """
    size = 2**m
    return (value%size)

def is_between(value, start, end, including_start=False, including_end=False):
    """
    Checks if a given value is in the range start to end while considering
    given options, i.e., including/excluding start and/or end of the range.
    :param value: Int
    :param start: Int
    :param end: Int
    :param including_start: Bool, default value = False
    :param including_end: Bool, default value = False
    :return:
    """
    if not including_start and not including_end:   # not include both start and end
        if (start < value < end):
            return True
        elif (start > end) and (start < value <= (2**m - 1) or 0 <= value < end):
            return True
        elif (start == end) and (value != start):
            return True
        return False
    elif not including_start and including_end:     # include end but not the start
        if value == end:
            return True
        elif (start < value <= end):
            return True
        elif (start > end) and ((start < value <= (2**m - 1)) or (0 <= value <= end)):
            return True
        elif (start == end) and (value != start):
            return True
        return False
    elif including_start and not including_end:     # include start but not the end
        if value == start:
            return True
        elif (start <= value < end):
            return True
        elif (start > end) and (start <= value <= (2**m - 1) or 0 <= value < end):
            return True
        elif (start == end) and (value != end):
            return False
        return False
    else:                                           # include both start and end
        if (start <= value <= end):
            return True
        elif (start > end) and (start <= value <= (2**m - 1) or 0 <= value <= end):
            return True
        elif start == end:
            return True
        return False
