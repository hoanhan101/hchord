#!usr/bin/env python3

"""
    server.py - Chord Server Class
    Author:
        - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
        - Hoanh An (hoanhan@bennington.edu)
    Date: 11/15/2017
"""

import zerorpc

from chord_instance import ChordInstance
from threading import Thread
from const import *
from utils import *

server_IP = '0.0.0.0'

if __name__ == '__main__':
    server_chord_instance = ChordInstance(server_IP, default_port, 1)
    server_chord_instance.print_finger_table()
    try:
        s = zerorpc.Server(server_chord_instance)
        s.bind("tcp://{0}:{1}".format(server_IP, default_port))
        s.run()
    except KeyboardInterrupt:
        print("Exit using KeyboardInterrupt")