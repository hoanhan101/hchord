#!usr/bin/env python3

"""
    client.py - Client Class
    Author:
        - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
        - Hoanh An (hoanhan@bennington.edu)
    Date: 11/15/2017
"""


import zerorpc

from chord_instance import ChordInstance
from const import *
from utils import *

client_IP = '127.0.0.1'
server_IP = '0.0.0.0'

client_chord_instance = ChordInstance(client_IP, default_port, 3)

try:
    c = zerorpc.Client()
    c.connect("tcp://{0}:{1}".format(server_IP, default_port))

    if c.ping_back():
        print("There is a connection. Start to join")
        server_chord_instance = deserialize(c.return_instance())
        server_chord_instance.print_finger_table()
        client_chord_instance.join(server_chord_instance)
        server_chord_instance.print_finger_table()
        client_chord_instance.print_finger_table()

except KeyboardInterrupt:
    print("Exit using KeyboardInterrupt")