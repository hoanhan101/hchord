#!/usr/bin/env python3

"""
    server.py - A TCP Server that can send and receive message.
    Author:
        - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
        - Hoanh An (hoanhan@bennington.edu)
    Date: 11/11/2017
"""

import socket
import threading

class ServerThread(threading.Thread):
    def __init__(self, IP, PORT, IP_TO_SEND=None, PORT_TO_SEND=None):
        threading.Thread.__init__(self)
        self.TCP_ADDRESS = IP
        self.TCP_PORT = PORT
        self.BUFFER_SIZE = 40
        self.IP_TO_SEND = IP_TO_SEND
        self.PORT_TO_SEND = PORT_TO_SEND
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def listen(self):
        self.s.bind((self.TCP_ADDRESS, self.TCP_PORT))

        while True:
            self.s.listen(1)

            conn, addr = self.s.accept()
            data = conn.recv(self.BUFFER_SIZE).decode()

            while data != "":
                print("{0}:{1} RECEIVED \"{2}\" FROM {3}".format(self.TCP_ADDRESS, self.TCP_PORT, data, addr[0]))
                data = conn.recv(self.BUFFER_SIZE).decode()

            conn.close()

    def send(self):
        self.s.connect((self.IP_TO_SEND, self.PORT_TO_SEND))

        while True:
            MESSAGE = input("Enter message: ")
            self.s.send(MESSAGE.encode())
            print('Sent {0} to {1}'.format(MESSAGE, self.IP_TO_SEND))

    def run(self):
        if self.IP_TO_SEND == None:
            self.listen()
            print("START LISTENING THREAD")
        else:
            self.send()
            print("START SENDING THREAD")

if __name__ == '__main__':
    server_1_listening_thread = ServerThread('0.0.0.0', 9000)
    server_1_sending_thread = ServerThread('0.0.0.0', 9000, IP_TO_SEND='10.2.24.63', PORT_TO_SEND=9000)

    server_1_listening_thread.start()
    server_1_sending_thread.start()
