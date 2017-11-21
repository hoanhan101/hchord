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

class Server(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        try:
            print("SERVER_THREAD IS RUNNING")
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
            print("CLIENT_THREAD IS RUNNING")
            your_IP = input("Enter IP to join: ")
            c = zerorpc.Client()
            c.connect("tcp://{0}:{1}".format(your_IP, default_port))

            if c.is_alive():
                instance_list = deserialize(c.get_instance_list())

                # append to a local list and join the first instance (can be anyone in the list)
                instance_list.append(my_chord_instance)
                my_chord_instance.join(instance_list[0])

                # update the instance list locally
                my_chord_instance.set_instance_list(serialize(instance_list))

                # update other instance list using RPC as well
                for instance in my_chord_instance.instance_list:
                    if instance.IP_ADDRESS != my_IP:
                        temp_client = zerorpc.Client()
                        temp_client.connect("tcp://{0}:{1}".format(instance.IP_ADDRESS, default_port))
                        temp_client.set_instance_list(serialize(instance_list))

        except KeyboardInterrupt:
            print("Exit using KeyboardInterrupt")

if __name__ == '__main__':
    my_IP = get_my_IP()

    # temporary instance list, use to startup a chord instance
    # real instance list is an attribute in chord instance
    instance_list = []

    my_chord_instance = ChordInstance(my_IP, default_port)
    instance_list.append(my_chord_instance)

    server = Server()
    client = Client()

    server.start()
    client.start()
