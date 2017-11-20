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

my_IP = '10.2.18.19'
my_PORT = default_port

# temporary instance list, use to startup a chord instance
# real instance list is an attribute in chord instance
instance_list = []

my_chord_instance = ChordInstance(my_IP, default_port)
instance_list.append(my_chord_instance)

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
            your_IP = input("Enter IP to join to : ")
            your_PORT = input('Enter the PORT of the node : ')
            c = zerorpc.Client()
            c.connect("tcp://{0}:{1}".format(your_IP, your_PORT))

            try:
                client_exists = c.is_alive()
            except:
                client_exists = False
            if client_exists:
                # instance_list = deserialize(c.get_instance_list())
                #
                # instance_list.append(my_chord_instance)
                # my_chord_instance.join(instance_list[0])
                #
                # # update my chord_instance list locally
                # my_chord_instance.set_instance_list(serialize(instance_list))
                n0 = deserialize(c.get_instance())
                my_chord_instance.join(n0)
            else:
                my_chord_instance.join(None)

            my_chord_instance.print_finger_table()

            # update other instance list
            # for instance in my_chord_instance.instance_list:
            #     if (instance.IP_ADDRESS != my_IP) and (instance.PORT != my_PORT):
            #         temp_client = zerorpc.Client()
            #         temp_client.connect("tcp://{0}:{1}".format(instance.IP_ADDRESS, instance.PORT))
            #         temp_client.set_instance_list(serialize(instance_list))

        except KeyboardInterrupt:
            print("Exit using KeyboardInterrupt")
        except Exception as e:
            print('Invalid Input! Terminating program...')

if __name__ == '__main__':
    server = Server()
    client = Client()

    server.start()
    client.start()
