from const import m

def constrain(value):
    """
        Returns a value modulo 2^m. Used to wrap the value between 0 and 2^m.
    """
    size = 2**m
    return (value%size)

def is_between(value, start, end, including_start=False, including_end=False):
    """
        Checks if a given value is in the range start to end while considering
        given options, i.e., including/excluding start and/or end of the range.
        params:
            start: int
            end: int
            including_start: bool, default value = False
            including_end: bool, default value = False
    """
    if not including_start and not including_end:
        # not include both start and end
        if (start < value < end):
            return True
        elif (start > end) and (start < value <= (2**m - 1) or 0 <= value < end):
            return True
        elif (start == end) and (value != start):
            return True
        return False
    elif not including_start and including_end:
        # include end but not the start
        if value == end:
            return True
        elif (start < value <= end):
            return True
        elif (start > end) and ((start < value <= (2**m - 1)) or (0 <= value <= end)):
            return True
        elif (start == end) and (value != start):
            return True
        return False
    elif including_start and not including_end:
        # include start but not the end
        if value == start:
            return True
        elif (start <= value < end):
            return True
        elif (start > end) and (start <= value <= (2**m - 1) or 0 <= value < end):
            return True
        elif (start == end) and (value != end):
            return False
        return False
    else:
        # include both start and end
        if (start <= value <= end):
            return True
        elif (start > end) and (start <= value <= (2**m - 1) or 0 <= value <= end):
            return True
        elif start == end:
            return True
        return False
