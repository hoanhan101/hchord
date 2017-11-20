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
from const import *
from utils import *

server_IP = '0.0.0.0'

instance_list = []

if __name__ == '__main__':
    server_chord_instance_1 = ChordInstance(server_IP, default_port, 1)
    # server_chord_instance_3 = ChordInstance(server_IP, default_port, 3)
    # server_chord_instance_6 = ChordInstance(server_IP, default_port, 6)

    instance_list.append(server_chord_instance_1)
    # instance_list.append(server_chord_instance_3)
    # instance_list.append(server_chord_instance_6)

    # server_chord_instance_3.join(instance_list[0])
    # server_chord_instance_6.join(instance_list[0])

    server_chord_instance_1.instance_list = instance_list

    for instance in server_chord_instance_1.instance_list:
        instance.print_finger_table()

    try:
        print("SERVER IS RUNNING")
        s = zerorpc.Server(server_chord_instance_1)
        s.bind("tcp://{0}:{1}".format(server_IP, default_port))
        s.run()
    except KeyboardInterrupt:
        print("Exit using KeyboardInterrupt")