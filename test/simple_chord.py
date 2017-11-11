#!/usr/bin/env python3
"""
    simple_chord.py - Implemented Chord as my understanding, without research paper
    Author:
        - Hoanh An (hoanhan@bennington.edu)
    Date: 11/3/2017
"""
import hashlib

m = 3

class Node:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.ID = chord_hash("{0}:{1}".format(IP, PORT))
        self.finger_table = self.create_finger_table(m)

    def create_finger_table(self, number_of_entries):
        finger_table = []
        for i in range(number_of_entries):
            start_value = self.ID + 2**i
            finger_table.append({'start_value': start_value})
        for i in range(number_of_entries):
            range_start = finger_table[i]['start_value']
            if i != number_of_entries - 1:
                range_end = finger_table[i + 1]['start_value']
            else:
                range_end = finger_table[0]['start_value'] - 1
            finger_table[i]['range_start'] = range_start
            finger_table[i]['range_end'] = range_end
            finger_table[i]['successor'] = self.ID
        return finger_table

    def to_dict(self):
        print("ID: {0}, IP: {1}, PORT: {2}".format(self.ID, self.IP, self.PORT))

        # Print Finger Table
        for i in self.finger_table:
            print('{0} | [{1}, {2}) | {3}'.format(i['start_value'], i['range_start'], i['range_end'], i['successor']))

    def is_between(self, value, start, end, including_start=False, including_end=False):
        """
        Check if value in the range.
        :param value:
        :param value:
        :param value:
        :return: True if value is in the range
        """
        print('Node {0}.is_between(val={1}, start={2}, end={3}, include_start={4}, include_end={5})'.format(self.ID, value,
                                                                                                       start, end,
                                                                                                       including_start,
                                                                                                       including_end))
        if not including_start and not including_end:
            # not include both start and end
            if (start < value < end):
                return True
            elif (start > end) and (start < value <= (2 ** m - 1) or 0 <= value < end):
                return True
            return False
        elif not including_start and including_end:
            # include end but not the start
            # print("not including_start and including_end passed_2")
            if (start == end):
                return True
            elif (start < value <= end):
                return True
            elif (start > end) and ((start < value <= (2 ** m - 1)) or (0 <= value <= end)):
                return True
            return False
        elif including_start and not including_end:
            # include start but not the end
            if (start <= value < end):
                return True
            elif (start > end) and (start <= value <= (2 ** m - 1) or 0 <= value < end):
                return True
            elif (start == end):
                return True
            return False
        else:
            # include both start and end
            if (start <= value <= end):
                return True
            elif (start > end) and (start <= value <= (2 ** m - 1) or 0 <= value <= end):
                return True
            elif (start == end):
                return True
        return False

def chord_hash(input_string):
    """
    Use SHA-1 hash to hash a string, return a value that in the range 2^m

    Steps:
    - Hash a string to get hex string
    - Convert it to integer
    - Shift right (160 - m) places

    Why shifting right (160 - m) places:
        - Shifting right m places equals to dividing 2^m.
        - Given m and a value 2^160, in order to find 2^m, need to need to divide 2^160 by 2^(160-m)

    :param input_string: String to hash
    :return: Hash of the string
    """
    h = hashlib.sha1()  # 160 bit string
    encoded_data = input_string.encode('utf-8')
    h.update(encoded_data)
    hex_string = h.hexdigest()
    hex_value = int(hex_string, 16)
    hash_integer_value = hex_value >> (160 - m)
    return hash_integer_value



if __name__ == '__main__':
    node_1 = Node('0.0.0.0', 9000)
    node_1.to_dict()

    node_2 = Node('192.168.1.1', 9001)
    node_2.to_dict()

    # node_3 = Node('192.168.0.0', 9002)
    # node_3.join(None)
    # node_3.to_dict()


