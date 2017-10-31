#!/usr/bin/env python3
"""
        FingerTable.py - A class defining a finger table. Each chord
            server maintains one finger table
        Author: Nidesh Chitrakar
        Date: 10/30/2017
"""
import math

class Node(object):
    def __init__(self,ID,m):
        self.ID = ID
        self.m = m
        self.finger_table = FingerTable(self, m)

class FingerTable:
    # m = 3 # num of rows // key space size
    # start_values = [0] * m
    # range_start = [0] * m
    # range_end = [0] * m
    # successors = [0] * m

    def __init__(self, NODE, m):
        self.m = m
        self.start_values = [0] * m
        self.range_start = [0] * m
        self.range_end = [0] * m
        self.successors = [0] * m
        for i in range(0,m):
            self.start_values[i] = int(NODE.ID + math.pow(2,i))
        for i in range(0,m):
            #start_values[i] = NODE.ID + math.pow(2,i)
            self.range_start[i] = self.start_values[i]
            if (i + 1 == m):
                self.range_end[i] = NODE.ID
            else:
                self.range_end[i] = self.start_values[i+1]
            self.successors[i] = 0 # NODE

    def print_table(self):
        for i in range(0,self.m):
            print(self.start_values[i], self.range_start[i], self.range_end[i], self.successors[i])

if __name__ == '__main__':
    node = Node(1,4)
    node.finger_table.print_table()
