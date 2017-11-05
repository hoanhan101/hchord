#!usr/bin/env python3
"""
    ChordApp.py
    Author: Nidesh Chitrakar
    Date:
"""
m = 3

class Node():
    def __init__(self, IP_ADDRESS, PORT, ID):
        self.IP_ADDRESS = IP_ADDRESS
        self.PORT = PORT
        self.ID = ID

    def to_dict(self):
        return 'ID: {0}, IP: {1}, PORT: {2}'.format(self.ID, self.IP, self.PORT)

class ChordInstance(object):
    def __init__(self, IP_ADDRESS, PORT, NODE, ID):
        self.IP_ADDRESS = IP_ADDRESS
        self.PORT = PORT
        self.NODE = Node(IP_ADDRESS, PORT, ID)

        self.ID = ID
        #if (NODE != None):
            #self.NODE.join(NODE.ID)
        self.finger_table = self.create_finger_table()
        self.successor = self.finger_table[0]['successor'] #self.NODE
        #self.predecessor = None

    def create_finger_table(self):
        finger_table = []
        for i in range(0,m):
            finger_table.append({})
            finger_table[i]['start'] = self.NODE.ID + (2**i)
        for i in range(0,m):
            finger_table[i]['range_start'] = finger_table[i]['start']
            if (i != m - 1):
                finger_table[i]['range_end'] = finger_table[i+1]['start']
            else:
                finger_table[i]['range_end'] = self.NODE.ID
            finger_table[i]['successor'] = self.NODE.ID
        return finger_table

    #def join(ID):

    def is_between(self,value, start, end, including_start=False, including_end=False):
        """
            @params:
                start: Int
                end: Int
                including_start: bool
                including_end: bool
        """
        if not including_start and not including_end:
            # not include both start and end
            if (start < value < end):
                return True
            elif (start > end) and (start < value <= (2**m - 1) or 0 <= value < end):
                return True
            return False
        elif not including_end and including_end:
            # include end but not the start
            if (start < value <= end):
                return True
            elif (start > end) and (start < value <= (2**m - 1) or 0 <= value <= end):
                return True
            return False
        elif including_start and not including_end:
            # include start but not the end
            if (start <= value < end):
                return True
            elif (start > end) and (start <= value <= (2**m - 1) or 0 <= value < end):
                return True
            return False
        else:
            # include both start and end
            if (start <= value <= end):
                return True
            elif (start > end) and (start <= value <= (2**m - 1) or 0 <= value <= end):
                return True
            elif (start == end):
                return True
            return False

    def find_successor(self, ID):
        n0 = self.find_predecessor(ID)
        return n0.successor

    def find_predecessor(self,ID):
        n0 = self
        while not self.is_between(ID, n0.ID, n0.successor, including_end=True):
            print(ID, n0.ID, n0.successor)
            n0 = n0.closest_preceding_node(ID)
        return n0

    def closest_preceding_node(self, ID):
        for i in range(m-1, -1, -1):    # from i = m downto 1
            if self.is_between(self.finger_table[i]['successor'], self.ID, ID):
                return self.finger_table[i]['successor']
        return self

    def print_finger_table(self):
        for i in range (0,m):
            print self.finger_table[i]

if __name__ == '__main__':
    chord1 = ChordInstance('0.0.0.0', 9000, None, 1)
    # print(chord1.is_between(7,6,1))
    # print(chord1.is_between(0,6,1,including_start=True))
    # print(chord1.is_between(5,6,1,including_start=True))
    # print(chord1.is_between(3,3,7,including_start=True, including_end=True))
    # print(chord1.is_between(3,4,2,including_start=True))
    chord1.print_finger_table()
    print(chord1.find_successor(5))
