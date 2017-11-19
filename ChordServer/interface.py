import zerorpc
from chord_instance import ChordInstance
from threading import Thread
from const import default_port
import socket
import pickle

class Listener(Thread):
    def __init__(self, CHORD_INSTANCE):
        Thread.__init__(self)
        self.port = default_port
        query = input('Would you like to use the default port (9000)? (Y/N) : ')
        if query.lower() == 'n':
            self.port = int(input('Please enter a port : '))
        self.server = zerorpc.Server(CHORD_INSTANCE)
        self.server.bind('{0}{1}'.format('tcp://0.0.0.0:',self.port))
        self.server.run()

class Sender(Thread):
    def __init__(self, CHORD_INSTANCE):
        Thread.__init__(self)
        IP_ADDRESS = input('Enter the IP address of desired node to join to : ')
        PORT = int(input('Enter the port of desired node to join to : '))
        self.client = zerorpc.Client()
        try:
            self.client.connect('tcp://{0}:{1}'.format(IP_ADDRESS, PORT))
            if not (self.client.ping_back()):
                print('Sorry no such node exists. Creating a new ring...')
            else:
                print('Joining to the ring...')
                NODE = pickle.loads(self.client.return_instance())
                CHORD_INSTANCE.join(NODE)
                CHORD_INSTANCE.print_finger_table()
        except Exception:
            print(Exception)

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    port = 9000

    chord_inst = ChordInstance(ip, port, 3)
    try:
        server = Listener(chord_inst)
        server.start()

        #
        # client = Sender(chord_inst)
        # c

    except KeyboardInterrupt:
        print('exited successfully...')
