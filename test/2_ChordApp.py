#!usr/bin/env python3
"""
    ChordApp.py
    Author: Nidesh Chitrakar
    Date:
"""
m = 3   # KEY_SPACE_SIZE (max 64)
NODE_LIST = []

class Node():
    def __init__(self, IP_ADDRESS, PORT, ID):
        self.IP_ADDRESS = IP_ADDRESS
        self.PORT = PORT
        self.ID = ID

    def to_dict(self):
        return 'ID: {0}, IP: {1}, PORT: {2}'.format(self.ID, self.IP, self.PORT)


class ChordInstance(object):
    def __init__(self, IP_ADDRESS, PORT, ID):
        self.IP_ADDRESS = IP_ADDRESS
        self.PORT = PORT
        self.NODE = Node(IP_ADDRESS, PORT, ID)
        self.ID = ID
        #self.finger_table = []
        self.finger_table = self.create_finger_table()
        #self.successor = self.finger_table[0]['successor'] #self.NODE
        self.successor = self
        self.predecessor = self

    def create_finger_table(self):
        finger_table = []
        for i in range(0,m):
            finger_table.append({})
            finger_table[i]['start'] = self.constrain(self.NODE.ID + (2**i))
        # for i in range(0,m):
        #     finger_table[i]['range_start'] = finger_table[i]['start']
        #     if (i != m - 1):
        #         finger_table[i]['range_end'] = finger_table[i+1]['start']
        #     else:
        #         finger_table[i]['range_end'] = self.NODE.ID
        #     finger_table[i]['successor'] = self
            finger_table[i]['successor'] = self
        return finger_table

    def constrain(self,value):
        # temp = 0
        size = 2**m
        # if value < 0:
        #     temp = size + value
        # elif value > size-1:
        #     temp = value - size
        # else:
        #     temp = value
        # return temp
        return (value%size)

    def print_finger_table(self):
        print('finger_table of node {0}'.format(self.ID))
        for i in range (0,m):
            # print(self.finger_table[i]['start'], self.finger_table[i]['range_start'],self.finger_table[i]['range_end'], self.finger_table[i]['successor'].ID)
            print(self.finger_table[i]['start'], self.finger_table[i]['successor'].ID)

    #def join(ID):

    def is_between(self,value, start, end, including_start=False, including_end=False):
        """
            @params:
                start: Int
                end: Int
                including_start: bool
                including_end: bool
        """
        print('Node{0}.is_between(val={1},start={2},end={3},include_start={4},include_end={5})'.format(self.ID,value,start,end,including_start,including_end))
        if not including_start and not including_end:
            # not include both start and end
            if (start < value < end):
                return True
            elif (start > end) and (start < value <= (2**m - 1) or 0 <= value < end):
                return True
            # elif (start == end) and (value != start):
            #     return True
            elif (start == end) and (value != start):
                return True
            return False
        elif not including_start and including_end:
            # include end but not the start
            #print("not including_start and including_end passed_2")
            if value == end:
                return True
            elif (start == end) and (value != start):
                return True
            elif (start < value <= end):
                return True
            elif (start > end) and ((start < value <= (2**m - 1)) or (0 <= value <= end)):
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
            elif (start == end) and value != end:
                return False
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
        print('Node{0}.find_successor({1}): finding successor of ID {2}'.format(self.ID,ID,ID))
        n0 = self.find_predecessor(ID)
        # print('-> Successor: {0}'.format(n0.successor.ID))
        # return n0.successor
        print('-> Successor: {0}'.format(n0.finger_table[0]['successor'].ID))
        return n0.finger_table[0]['successor']

    def find_predecessor(self,ID):
        print('Node{0}.find_predecessor({1}): finding predecessor of ID {2}'.format(self.ID,ID,ID))
        # if (self.ID == self.successor.ID):
        #     return self # self is the only node in the ring
        n0 = self
        # while not self.is_between(ID, n0.ID, n0.successor.ID, including_end=True):
        while not self.is_between(ID, n0.ID, n0.finger_table[0]['successor'].ID, including_end=True):
            #print(ID, n0.ID, n0.successor.ID)
            n0 = n0.closest_preceding_node(ID)
        print('-> Predecessor: {0}'.format(n0.ID))
        return n0

    def closest_preceding_node(self, ID):
        print('Node{0}.closest_preceding_node({1}): finding closest_preceding_node of ID {2}'.format(self.ID,ID,ID))
        n = m-1
        for i in range(n, -1, -1):    # from i = m downto 1
            print(' -> i = {0}'.format(i))
            if self.is_between(self.finger_table[i]['successor'].ID, self.ID, ID):
                return self.finger_table[i]['successor']
        return self

    def join(self, NODE):
        print('')
        print('Node{0}.join({1}): joining {2} to {3}'.format(self.ID,NODE,self.ID,NODE))
        print('')
        NODE_LIST.append(self)
        if (NODE != None):
            self.init_finger_table(NODE)
            self.update_others()
            # s = self.successor  #get successor
            for i in range(1,m):
                self.predecessor.update_finger_table(self,i)
        else:
            for i in range(0,m):
                self.finger_table[i]['successor'] = self
            self.predecessor = self

    def init_finger_table(self, NODE):
        print('Node{0}.init_finger_table({1}): init finger_table of node {2}'.format(self.ID,NODE.ID,self.ID))
        self.finger_table[0]['successor'] = NODE.find_successor(self.finger_table[0]['start'])
        # if self.is_between(self.ID,NODE.finger_table[0]['start'],NODE.finger_table[0]['successor'].ID):
        #     NODE.finger_table[0]['successor'] = self
        self.successor = self.finger_table[0]['successor']
        print('-> updated successor of finger_table[0][\'successor\'] of node {0} to {1}'.format(self.ID,self.finger_table[0]['successor'].ID))
        self.predecessor = self.successor.predecessor
        self.successor.predecessor = self
        self.predecessor.successor = self
        self.predecessor.finger_table[0]['successor'] = self
        # if self.is_between(self.ID,self.predecessor.finger_table[0]['start'],NODE.finger_table[0]['successor'].ID):
        #      self.predecessor.finger_table[0]['successor'] = self
        #self.predecessor.finger_table[0]['successor'] = self
        print('-> set predecessor of node {0} to {1}'.format(self.ID, self.predecessor.ID))
        print('-> set predecessor of node {1} to {0}'.format(self.ID, self.finger_table[0]['successor'].ID))

        for i in range(0,m-1):
        #for i in range(m-2,-1,-1):
            print('i = {0}'.format(i))
            self.print_finger_table()
            # if self.is_between(self.finger_table[i+1]['start'], self.ID, self.finger_table[i]['successor'].ID, including_start=True, including_end=True):
            if self.is_between(self.finger_table[i+1]['start'], self.ID, self.finger_table[i]['successor'].ID, including_start=True):
                print('Value {0} is in [{1},{2}]'.format(self.finger_table[i+1]['start'],self.ID,self.finger_table[i]['successor'].ID))
                self.finger_table[i+1]['successor'] = self.finger_table[i]['successor']
                print('-> updated the successor of finger_table[{0}][\'successor\'] of Node {1} to {2}'.format(i+1,self.ID,self.finger_table[i]['successor'].ID))
            else:
                print('Value {0} is not in [{1},{2}]'.format(self.finger_table[i+1]['start'],self.ID,self.finger_table[i]['successor'].ID))
                self.finger_table[i+1]['successor'] = NODE.find_successor(self.finger_table[i+1]['start'])
                print('-> updated the successor of finger_table[{0}][\'successor\'] of Node {1} to {2}'.format(i+1,self.ID,NODE.find_successor(self.finger_table[i-1]['start']).ID))
        #print('-> Updating finger_table of Node {0}\'s predecessor {1}'.format(self.ID, self.predecessor.ID))
        # for j in range(1,m):
        #     self.predecessor.update_finger_table(self,j)
        # self.print_finger_table()
        # self.predecessor.update_others()

    def update_others(self):
        print('Node{0}.update_others(): update finger_table of other nodes'.format(self.ID))
        for i in range(0,m):
            val = self.constrain(self.ID - 2**(i))
            print('find predecessor of={1}, val={0}'.format(val, self.ID - 2**(i)))
            p = self.find_predecessor(val)
            #n = self.find_node(val)
            print('predecessor of {0} is {1}'.format(val, p.ID))
            print('Update finger table of Node {0}'.format(p.ID))
            if (p != self):
                p.update_finger_table(self, i)
            else:
                p = p.predecessor
                p.update_finger_table(self,i)
            #self.predecessor.update_finger_table(self,i)

    def find_node(self, ID):
        # initital plan: find node of some ID. if it doesn't exist then it returns None
        # current implementation: checks if a node with given ID exists. if it does then it returns the node
        #                         works by looping through a global list of nodes in the ring
        for node in NODE_LIST:
            if (ID == node.ID):
                return node
        return None

    def update_finger_table(self, NODE, i):
        print('Node{0}.update_finger_table({1}, {2})'.format(self.ID, NODE.ID, i))
        #if self.is_between(NODE.ID,self.ID, self.finger_table[i]['successor'].ID, including_start=True):
        if self.is_between(NODE.ID,self.finger_table[i]['start'], self.finger_table[i]['successor'].ID, including_start=True):
        #if self.is_between(NODE.ID,self.finger_table[i]['range_start'], self.finger_table[i]['range_end'], including_start=True):
            self.finger_table[i]['successor'] = NODE
            print('-> updated the value of finger_table[{0}][\'successor\'] of Node {1} to {2}'.format(i,self.ID,NODE.ID))
        # else:
        #     p = self.predecessor
        #     if (p != NODE):
        #         print('@update_finger_table: p = {0}'.format(p.ID))
        #         p.update_finger_table(NODE, i)
        #         self.print_finger_table()
            p = self.predecessor
            if (p != NODE):
                print('@update_finger_table: p = {0}'.format(p.ID))
                p.update_finger_table(NODE, i)
                self.print_finger_table()




if __name__ == '__main__':
    chord1 = ChordInstance('0.0.0.0', 9000, 4)
    chord2 = ChordInstance('127.0.0.1', 9001, 0)
    chord3 = ChordInstance('192.168.1.1', 9002, 1)
    # chord4 = ChordInstance('192.168.1.1', 9003, 13)
    # chord5 = ChordInstance('192.168.1.1', 9004, 255)
    # chord6 = ChordInstance('192.168.1.1', 9005, 35000)
    # chord1.print_finger_table()
    # chord2.print_finger_table()
    # chord3.print_finger_table()
    # chord4.print_finger_table()
    chord1.join(None)
    chord2.join(chord1)
    # chord1.print_finger_table()
    # chord2.print_finger_table()
    # #print('successor of node 1 = {0}'.format(chord1.successor.ID))
    chord3.join(chord2)
    # chord1.print_finger_table()
    # chord2.print_finger_table()
    # chord3.print_finger_table()
    # chord4.join(chord2)
    # chord5.join(chord4)
    # chord6.join(chord3)
    # # print(chord1.is_between(7,6,1))
    # # print(chord1.is_between(0,6,1,including_start=True))
    # # print(chord1.is_between(5,6,1,including_start=True))
    # # print(chord1.is_between(3,3,7,including_start=True, including_end=True))
    # # print(chord1.is_between(3,4,2,including_start=True))
    chord1.print_finger_table()
    chord2.print_finger_table()
    chord3.print_finger_table()
    # chord4.print_finger_table()
    # chord5.print_finger_table()
    # chord6.print_finger_table()
    # nodes = [chord1,chord2,chord3,chord4,chord5,chord6]
    # for node in nodes:
    #     print(' >> Node {0}\'s successor is node {1}.'.format(node.ID,node.successor.ID))
    # print(chord1.finger_table[0]['successor'].ID)
    # print(chord1.successor.ID)
