#!/usr/bin/env python3
"""
    Chord.py - Implementation of MIT's Chord Distributed Hash Table (DHT)
    Author:
        - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
        - Hoanh An (hoanhan@bennington.edu)
    Date: 10/29/2017
"""
import hashlib

m = 3

class Node:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.ID = chord_hash("{0}:{1}".format(IP, PORT))

    def to_dict(self):
        print("ID: {0}, IP: {1}, PORT: {2}".format(self.ID, self.IP, self.PORT))

class ChordInstance:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.ID = chord_hash("{0}:{1}".format(IP, PORT))
        self.predecessor = None
        self.successor = None
        self.finger_table = self.init_finger_table(m)

    def init_finger_table(self, m):
        finger_table = []
        return finger_table

    def create_identifier_space(self):
        for i in range(2**m):
            print(i)

    def to_dict(self):
        print("ID: {0}, IP: {1}, PORT: {2}".format(self.ID, self.IP, self.PORT))

    def join(self, Node):
        print("ID: {0}, IP: {1}, PORT: {2} is joining".format(Node.ID, Node.IP, Node.PORT))

def chord_hash(input_string):
    """
    Use SHA-1 hash to hash a string, convert it to integer and shift right 160 - m places

    Why shifting right 160 - m places:
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

def is_between(target_value, start_value, end_value):
    """
    Check if target value in the range of [start_value, end_value)
    :param target_value:
    :param start_value:
    :param end_value:
    :return: True if target value is in the range
    """
    if target_value >= start_value and target_value < 2:
        return True
    return False

if __name__ == '__main__':
    # start new ring
    chord_instance = ChordInstance('0.0.0.0', 9000)
    chord_instance.to_dict()

    # join ring
    node_2 = Node('192.168.1.1', 9001)
    chord_instance.join(node_2)

