#!/usr/bin/env python3
"""
    chord_1.py - Implementation of MIT's Chord Distributed Hash Table (DHT)
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
        # self.predecessor = None
        # self.successor = None
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
            finger_table[i]['successor'] = None
        return finger_table

    def to_dict(self):
        print("")
        print("[*] ID: {0}, IP: {1}, PORT: {2}".format(self.ID, self.IP, self.PORT))
        # print("[*] Predecessor: {0}, Successor: {1}".format(self.predecessor, self.successor))
        print("[*] Finger Table: {0}".format(self.finger_table))
        print("")

    def join(self, Node=None):
        if Node:
            print("[+] ID: {0}, IP: {1}, PORT: {2} is joining".format(self.ID, self.IP, self.PORT))
            self.init_finger_table(Node)
            self.update_others()

        else:
            for i in range(m):
                # self.finger[i].node = self
                print("OK")
            # self.predecessor = self

    def init_finger_table(self, Node):
        print("[+] ID: {0}, IP: {1}, PORT: {2} is initializing finger table".format(self.ID, self.IP, self.PORT))

    def update_others(self):
        print("[+] ID: {0}, IP: {1}, PORT: {2} is updating others".format(self.ID, self.IP, self.PORT))

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

def is_between(target_value, start_value, end_value):
    """
    Check if target value in the range of [start_value, end_value)
    :param target_value:
    :param start_value:
    :param end_value:
    :return: True if target value is in the range
    """
    if target_value >= start_value and target_value < end_value:
        return True
    return False

if __name__ == '__main__':
    # start new ring
    node_1 = Node('0.0.0.0', 9000)
    node_1.to_dict()

    # join ring
    node_2 = Node('192.168.1.1', 9001)
    node_2.join(node_1)
    node_2.to_dict()

    node_3 = Node('192.168.0.0', 9002)
    node_3.join(None)
    node_3.to_dict()
