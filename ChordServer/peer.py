#!usr/bin/env python3

"""
    peer.py - A Peer acts as a Server and a Client
    Author:
        - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
        - Hoanh An (hoanhan@bennington.edu)
    Date: 11/15/2017
"""

import zerorpc

from chord_instance import ChordInstance
from const import *
from utils import *
from threading import Thread

my_IP = '0.0.0.0'

instance_list = []

# when startup
my_chord_instance = ChordInstance(my_IP, default_port, 1)
instance_list.append(my_chord_instance)
my_chord_instance.instance_list = instance_list

class Server(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        try:
            print("SERVER IS RUNNING")
            s = zerorpc.Server(my_chord_instance)
            s.bind("tcp://{0}:{1}".format(my_IP, default_port))
            s.run()
        except KeyboardInterrupt:
            print("Exit using KeyboardInterrupt")

class Client(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        try:
            your_IP = input("Which IP: ")
            c = zerorpc.Client()
            c.connect("tcp://{0}:{1}".format(your_IP, default_port))

            if c.is_alive():
                instance_list = deserialize(c.get_instance_list())

                instance_list.append(my_chord_instance)
                my_chord_instance.join(instance_list[0])

                c.set_instance_list(serialize(instance_list))
                my_chord_instance.set_instance_list(serialize(instance_list))

                for instance in my_chord_instance.instance_list:
                    instance.print_finger_table()

        except KeyboardInterrupt:
            print("Exit using KeyboardInterrupt")

if __name__ == '__main__':
    server = Server()
    server.start()

    client = Client()
    client.start()

    # server_chord_instance_3 = ChordInstance(my_IP, default_port, 3)
    # server_chord_instance_6 = ChordInstance(my_IP, default_port, 6)

    # instance_list.append(server_chord_instance_3)
    # instance_list.append(server_chord_instance_6)

    # server_chord_instance_3.join(instance_list[0])
    # server_chord_instance_6.join(instance_list[0])

    # for instance in my_chord_instance.instance_list:
    #     instance.print_finger_table()

