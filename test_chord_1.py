#!/usr/bin/env python3
"""
    Chord.py - Implementation of MIT's Chord Distributed Hash Table (DHT)
    Author:
        - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
        - Hoanh An (hoanhan@bennington.edu)
    Date: 10/29/2017
"""
import hashlib

IP_ADDRESS = '127.0.0.1'
PORT = 9000
KEY_SPACE_SIZE = 16 # m, number of row in finger_table

class Node(object):
    def __init__(self, ID, IP_ADDRESS, PORT):
        self.ID = ID
        self.IP_ADDRESS = IP_ADDRESS
        self.PORT = PORT

    def to_dict(self):
        return {'ID': self.ID, 'IP ADDRESS': self.IP_ADDRESS, 'PORT': self.PORT}

# class FingerTable(object):
#     def do_something(self):
#         return True

class Chord(object):
    def __init__(self, IP_ADDRESS, PORT, ID, predecessor, successor, finger_table):
        self.IP_ADDRESS = IP_ADDRESS
        self.PORT = PORT
        self.ID = ID
        self.predecessor = Node
        self.successor = Node
        self.finger_table = [] # start_value, range_start, range_end, successor

    """
        Find the successor Node of an identifier ID
    """
    # ask node n to find IT's successor
    def find_successor(self, ID):
        n_prime = find_predecessor(ID)
        return n_prime.successor

    # ask node n to find ID's predecessor
    def find_predecessor(self, ID):
        n_prime = self
        while ID not in (n_prime, n_prime.successor): # more bounding
            n_prime = n_prime.closet_preceding_finger(ID)
        return n_prime

    # return closet finger preceding ID
    def closet_preceding_finger(self, ID):
        for i in range(KEY_SPACE_SIZE, 1, -1):
            if finger[i].node in (self, ID): # bounding
                return finger[i].node

    """
        Node join operation
    """
    # define successor finger[1].node

    # node n joins the network
    # n' is an arbitrary node in the network

    def join(self, n_prime):
        if n_prime:
            # move keys in (predecessor, n] from successor
            init_finger_table(n_prime)
            update_others()

        # n is the only node in the network
        else:
            for i in range(1, KEY_SPACE_SIZE):
                finger[i].node = n
            predecessor = n

    # initialize finger table of local node
    # n' is an arbitrary node already in the network
    def init_finger_table(self, n_prime):
        finger[1].node = n_prime.find_successor(finger[1].start)
        predecessor = successor.predecessor
        successor.predecessor = n
        for i in range(1, KEY_SPACE_SIZE - 1):
            if finger[i + 1].start in (n, finger[i].node): # bounding
                finger[i + 1].node = finger[i].node
            else:
                finger[i + 1].node = n_prime.find_successor(finger[i + 1].start)

    # update all nodes whose finger table should refer to n
    def update_others(self):
        for i in range(1, KEY_SPACE_SIZE):
            # find last node p whose ith finger might be n
            p = find_predecessor(n - 2**(i-1))
            p.update_finger_table(n, i)

    # if s is ith finger of n, update n's finger table with s
    def update_finger_table(self, s, i):
        if s in (n, finger[i].node): # bounding
            finger[i].node = s
            p = predecessor
            p.update_finger_table(s, i)

def chord_hash(input_string):
    h = hashlib.sha1()
    encoded_data = input_string.encode('utf-8')
    h.update(encoded_data)
    hex_string = h.hexdigest()
    return hex_string

if __name__ == '__main__':
    data = '{0}:{1}'.format(IP_ADDRESS, PORT)
    print(chord_hash(data))

    node1 = Node(1, IP_ADDRESS, PORT)

