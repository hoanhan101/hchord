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

my_IP = '127.0.0.1'
server_IP = '0.0.0.0'

my_chord_instance = ChordInstance(my_IP, default_port, 3)

try:
    c = zerorpc.Client()
    c.connect("tcp://{0}:{1}".format(server_IP, default_port))

    if c.is_alive():
        instance_list = deserialize(c.get_instance_list())

        instance_list.append(my_chord_instance)
        my_chord_instance.join(instance_list[0])

        c.set_instance_list(serialize(instance_list))

        for instance in instance_list:
            instance.print_finger_table()

except KeyboardInterrupt:
    print("Exit using KeyboardInterrupt")