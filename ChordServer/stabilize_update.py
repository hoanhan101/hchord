import threading
import randint
from const import m
from utils import *

class StabilizeUpdate(threading.Thread):
    def __init__(self, chord_instance):
        threading.Thread.__init__(self)
        self.chord_instance = chord_instance

    def stabilize(self):
        n_0 = self.chord_instance.successor.predecessor
        if is_between(n_0.ID, self.chord_instance.ID, self.chord_instance.successor.ID):
            self.chord_instance.successor = n_0
        self.chord_instance.successor.notify(self)

    def notify(self, NODE):
        if ((self.chord_instance.predecessor == None) or is_between(NODE.ID, self.chord_instance.predecessor.ID, self.chord_instance.ID)):
            self.chord_instance.predecessor = NODE

    def fix_fingers(self):
        i = randint(1,2**m)
        self.chord_instance.finger_table[i]['successor'] = self.chord_instance.find_successor(self.chord_instance.finger_table[i]['start'])

    def run(self):
        self.stabilize()
        self.fix_fingers()
