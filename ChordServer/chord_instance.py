#!usr/bin/env python3

"""
    chord_instance.py - A Chord Instance Class
    Author:
        - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
        - Hoanh An (hoanhan@bennington.edu)
    Date: 10/30/2017
"""

from node import Node
from utils import *
from const import m
from random import randint
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc import client
import pickle
import zerorpc
import socket

class ChordInstance(object):
    """
    Each Chord Instance contains the information about its node and maintains
    a finger table, its successor, and its predecessor.
    """
    def __init__(self, IP_ADDRESS, PORT, ID):
        """
        Initialize a ChordInstance.
        :param IP_ADDRESS: String
        :param PORT: Int
        :param ID: Int
        """
        self.IP_ADDRESS = IP_ADDRESS
        self.PORT = PORT
        self.NODE = Node(IP_ADDRESS, PORT, ID)
        #self.ID = self.NODE.ID
        self.ID = ID
        self.finger_table = self.create_finger_table()

        # set own successor and predecessor to self, i.e., the node is unattached
        self.successor = self
        self.predecessor = self

    def ping_back(self):
        return True

    def get_ID(self):
        return self.ID

    def set_ID(self, value):
        self.ID = value
        # return self.ID

    def return_instance(self):
        return pickle.dumps(self)

    def get_successor(self):
        return self.successor.ID

    def set_successor(self, i, dict):
        self.print_finger_table()
        temp_dict = pickle.loads(dict.data)
        self.finger_table[i]['successor'] = temp_dict
        self.print_finger_table()

    def create_finger_table(self):
        """
        Create a simple finger table of size m*2 with the start values generated
        by ID + 2^i where 0 <= i < m.
        All the successor values are set to self, i.e., the chord instance does
        not know about other nodes in the ring.
        :return: Finger Table
        """
        finger_table = []
        for i in range(0,m):
            finger_table.append({})
            finger_table[i]['start'] = constrain(self.NODE.ID + (2**i))
            finger_table[i]['successor'] = self
        return finger_table

    def print_finger_table(self):
        """
        Prints the finger table of a node.
        :return: None
        """
        print('finger_table of node {0}'.format(self.ID))
        print("successor: {0}, predecessor: {1}".format(self.successor.ID, self.predecessor.ID))
        for i in range (0,m):
            print(self.finger_table[i]['start'], self.finger_table[i]['successor'].ID)


    def find_successor(self, ID):
        """
        Find successor of a given ID.
        :param ID: Int
        :return: Node
        """
        print('Node{0}.find_successor({1}): finding successor of ID {2}'.format(self.ID,ID,ID))
        n0 = self.find_predecessor(ID)
        print('-> Successor: {0}'.format(n0.finger_table[0]['successor'].ID))
        return n0.finger_table[0]['successor']

    def find_predecessor(self,ID):
        """
        Find predecessor of a given ID.
        :param ID: Int
        :return: Node
        """
        print('Node{0}.find_predecessor({1}): finding predecessor of ID {2}'.format(self.ID,ID,ID))
        n0 = self
        while not is_between(ID, n0.ID, n0.finger_table[0]['successor'].ID, including_end=True):
            n0 = n0.closest_preceding_node(ID)
        print('-> Predecessor: {0}'.format(n0.ID))
        return n0

    def closest_preceding_node(self, ID):
        """
        Find the closest preceding node of a given ID.
        :param ID: Int
        :return: Node
        """
        print('Node{0}.closest_preceding_node({1}): finding closest_preceding_node of ID {2}'.format(self.ID,ID,ID))
        # from i = m-1 down to 0
        for i in range(m - 1, -1, -1):
            print(' -> i = {0}'.format(i))
            if is_between(self.finger_table[i]['successor'].ID, self.ID, ID):
                return self.finger_table[i]['successor']
        return self

    def join(self, NODE):
        """
        Join the network, given an arbitrary node in the network
        :param NODE: Node
        :return: None
        """
        print('')
        print('Node{0}.join({1}): joining {2} to {3}'.format(self.ID,NODE,self.ID,NODE))
        print('')
        if (NODE != None):
            self.init_finger_table(NODE)
            self.update_others()

            # MARK!!! DO WE NEED THIS?
            for i in range(1,m):
                self.predecessor.update_finger_table(self,i)
        else:
            for i in range(0,m):
                self.finger_table[i]['successor'] = self
            self.predecessor = self

    def init_finger_table(self, NODE):
        """
        Initialize finger table of local node, given an arbitrary node in the network.
        :param NODE: Node
        :return: None
        """
        print('Node{0}.init_finger_table({1}): init finger_table of node {2}'.format(self.ID,NODE.ID,self.ID))
        self.finger_table[0]['successor'] = NODE.find_successor(self.finger_table[0]['start'])
        self.successor = self.finger_table[0]['successor']
        print('-> updated successor of finger_table[0][\'successor\'] of node {0} to {1}'.format(self.ID,self.finger_table[0]['successor'].ID))
        self.predecessor = self.successor.predecessor
        self.successor.predecessor = self

        # MARK!!! WHY???
        self.predecessor.successor = self
        self.predecessor.finger_table[0]['successor'] = self
        print('-> set predecessor of node {0} to {1}'.format(self.ID, self.predecessor.ID))
        print('-> set predecessor of node {1} to {0}'.format(self.ID, self.finger_table[0]['successor'].ID))

        for i in range(0,m-1):
            print('i = {0}'.format(i))
            self.print_finger_table()
            if is_between(self.finger_table[i+1]['start'], self.ID, self.finger_table[i]['successor'].ID, including_start=True):
                print('Value {0} is in [{1},{2}]'.format(self.finger_table[i+1]['start'],self.ID,self.finger_table[i]['successor'].ID))
                self.finger_table[i+1]['successor'] = self.finger_table[i]['successor']
                print('-> updated the successor of finger_table[{0}][\'successor\'] of Node {1} to {2}'.format(i+1,self.ID,self.finger_table[i]['successor'].ID))
            else:
                print('Value {0} is not in [{1},{2}]'.format(self.finger_table[i+1]['start'],self.ID,self.finger_table[i]['successor'].ID))
                self.finger_table[i+1]['successor'] = NODE.find_successor(self.finger_table[i+1]['start'])
                print('-> updated the successor of finger_table[{0}][\'successor\'] of Node {1} to {2}'.format(i+1,self.ID,NODE.find_successor(self.finger_table[i-1]['start']).ID))

    def update_others(self):
        """
        Update all nodes whose finger tables should refer to itself.
        :return: None
        """
        print('Node{0}.update_others(): update finger_table of other nodes'.format(self.ID))
        for i in range(0,m):
            val = constrain(self.ID - 2**(i))
            print('find predecessor of={1}, val={0}'.format(val, self.ID - 2**(i)))
            p = self.find_predecessor(val)
            print('predecessor of {0} is {1}'.format(val, p.ID))
            print('Update finger table of Node {0}'.format(p.ID))

            # If p is not itself, which has already updated through init finger table,
            # then update finger tables of others
            if (p != self):
                p.update_finger_table(self, i)
            else:
                p = p.predecessor
                p.update_finger_table(self,i)

    def update_finger_table(self, NODE, i):
        """
        If a given node is ith finger of the node itself, update its finger table with that node
        :param NODE: A given node
        :param i: Int
        :return: None
        """
        print('Node{0}.update_finger_table({1}, {2})'.format(self.ID, NODE.ID, i))
        if is_between(NODE.ID,self.finger_table[i]['start'], self.finger_table[i]['successor'].ID, including_start=True):
            self.finger_table[i]['successor'] = NODE
            print('-> updated the value of finger_table[{0}][\'successor\'] of Node {1} to {2}'.format(i,self.ID,NODE.ID))
            p = self.predecessor
            if (p != NODE):
                print('@update_finger_table: p = {0}'.format(p.ID))
                p.update_finger_table(NODE, i)
                self.print_finger_table()

def generate_random_IP():
    START_RANGE = 0
    END_RANGE = 255

    random_int_1 = randint(START_RANGE, END_RANGE)
    random_int_2 = randint(START_RANGE, END_RANGE)
    random_int_3 = randint(START_RANGE, END_RANGE)
    random_int_4 = randint(START_RANGE, END_RANGE)

    random_IP = "{0}.{1}.{2}.{3}".format(random_int_1, random_int_2, random_int_3, random_int_4)
    return random_IP

def generate_random_port():
    START_RANGE = 0
    END_RANGE = 65535

    random_port_number = randint(START_RANGE, END_RANGE)
    return random_port_number

# if __name__ == '__main__':


    # my_ip = '10.2.18.108'
    # my_port = 9000
    # my_id = 5
    #
    # my_chord_instance = ChordInstance(my_ip, my_port, my_id)
    # my_chord_instance.set_ID(5)
    # print(my_chord_instance.get_ID())

    # server = SimpleXMLRPCServer((my_ip, my_port), allow_none=True)
    # server.register_instance(my_chord_instance)
    # server.serve_forever()

    # s = zerorpc.Server(my_chord_instance)
    # s.bind("tcp://0.0.0.0:9000")
    # s.run()

    # c = zerorpc.Client()
    # c.connect('tcp://10.2.19.113:9000')
    # print(c.get_id())







    # client_ip = '10.2.24.78'
    # client_port = 9001
    # client = xmlrpclib.Server('http://{0}:{1}'.format(client_ip, client_port))
    # if (client.ping_back()):
    #     print('ID: {0}, Successor: {1}, Predecessor: {2}'.format(client.ID, client.successor.ID, client.predecessor.ID))


    # NUMBER_OF_NODES = 3
    #
    # chord_instance_list = []
    # ID_list = []
    # collisions = 0
    #
    # startup_IP = '0.0.0.0'
    # startup_port = 0
    #
    # startup_chord_instance = ChordInstance(startup_IP, startup_port, 0)
    # startup_chord_instance.join(None)
    # ID_list.append(startup_chord_instance.ID)
    # chord_instance_list.append(startup_chord_instance)
    #
    # print(sorted(chord_instance_list))
    #
    # for i in range(NUMBER_OF_NODES - 1):
    #     temp_IP = generate_random_IP()
    #     temp_port = generate_random_port()
    #     rand_id = randint(1,2**m-1)
    #     temp_chord_instance = ChordInstance(temp_IP, temp_port, rand_id)
    #
    #     # Collisions Handling
    #     # If there already exists ID, pass. Otherwise, join.
    #     if temp_chord_instance.ID not in ID_list:
    #         ID_list.append(temp_chord_instance.ID)
    #         chord_instance_list.append(temp_chord_instance)
    #         temp_chord_instance.join(startup_chord_instance)
    #     else:
    #         collisions += 1
    #
    # print("")
    # print("============ <AFTER JOIN> ============")
    # print("")
    #
    # # Print fingers of all successful ChordInstance
    # for chord_instance in chord_instance_list:
    #     chord_instance.print_finger_table()
    #
    # # Collisions status
    # if collisions == 0:
    #     print("ID IS WELL DISTRIBUTED")
    # else:
    #     print("There exists {0} collisions".format(collisions))
    #
    # # Print out the sorted ID list
    # print('current list of nodes in ring: {0}'.format(sorted(ID_list)))
    #
    # # Check the number of successful instances
    # successful_instances = (NUMBER_OF_NODES - 1) - collisions
    #
    # if len(ID_list) == successful_instances:
    #     print("The number of successful instances is correct.")
    # else:
    #     print("Missing successful instances")
    #
    # for node in chord_instance_list:
    #     print('successor of node {0} is {1}'.format(node.ID, node.successor.ID))

