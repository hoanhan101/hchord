# Chord

![build-success](https://img.shields.io/badge/build-success-brightgreen.svg)
![test-passing](https://img.shields.io/badge/test-passing-brightgreen.svg)
![status-stable](https://img.shields.io/badge/status-stable-green.svg)

**Chord** is a 
[A Scalable Peer-to-peer Lookup Service for Internet
Applications](https://pdos.csail.mit.edu/papers/chord:sigcomm01/chord_sigcomm.pdf).
The goal of the project is to gain a better understanding of a lookup service
in distributed systems world.

## Project Status

There are 3 versions: ChordLocal, ChordServer and ChordServer (alt.). 
Details are provided below.

## Table of Contents

- [ChordLocal](#chordlocal)
  - [Files](#files)
  - [Testing](#testing)
- [ChordServer](#chordserver)
  - [Files](#files-1)
  - [Testing](#testing-1)
- [ChordServer (alt.)](#chordserver-alt)
  - [Files](#files-2)
  - [Testing](#testing-2)
- [TODO](#todo)

## ChordLocal

ChordLocal has the main Chord logic and can be used locally, which makes it easy for testing.

#### Files

- `chord_instance.py` is a Chord Instance class, which has main Chord logic as described in the paper.
- `const.py` has a constant key space size m.
- `node.py` is a Node class.
- `utils.py` contains helper functions.

#### Testing

- Tests are written using 32 nodes and key space size equals to 16,
but you can test it with as many nodes and as big key space size as you want.
- Configure the key space size in `const.py` under variable `m`.
- Configure the number of nodes in `chord_instance.py` under variable `NUMBER_OF_NODES`.
- Run `chord_instance.py`. 

## ChordServer

*This version is not working properly yet because of some strange behavior with RPC calls.
The alternative version below is working but is implemented in a hacky way.*

ChordServer implements TCP networking on top of ChordLocal, using RPC. We chose to use
 [zerorpc](http://www.zerorpc.io "zerorpc's Homepage") module for this purpose.

#### Files

- `peer.py` is a Peer class that acts as a server and a client. It has a thread to listen and another
one to use RPC. The server starts listening at the default port (9000) which can be modified in `const.py`.
- The client thread runs and asks the user which IP and port to connect to. The client then tries to connect
 to the given TCP address. If the client fails to find the server with that address in the network within 10
  seconds, then it will create a new ring with the server as the node.
- If the client is successful in connecting to a peer's server, then it will call its join function to that peer.
 Finger tables will be updated and a new node will be attached to our ring. 
- The algorithms for the joining and updated finger tables are discussed in detail in the paper.

#### Testing

The chord implementation with networking is located in the [ChordServer](/ChordServer) folder.

First change the `my_IP` variable in the `peer.py` file to your IP address.

Then you may want to change the key space value (m) in the `const.py` file to something large like 16, as with a small number
 of identifiers in the circle there is a higher chance of the hashed IDs colliding.
 
If you want to use a port other than 9000, then  you may do so by modifying the value of the `default_port` 
variable.
- `pip3 install zerorpc`
- `python3 peer.py`
- You will be asked to enter the IP adress and port of the peer you'd like to join to.
- The first node in the network will take approximately 10 seconds to initialize as the server times out after sending
continuous heartbeat messages and failing to connect to the given address. When it initializes, it begins listening for
any other peer in the network to join.
- You may then use the first node's IP address and port to connect to other nodes.

## ChordServer (alt.)

This is an alternative version of ChordServer. 
In this implementation, each Chord Instance maintains a list of every other Chord Instance in the ring.
That is not how Chord should work. However, until the main version is fixed and working properly,
just leave it here as a reminder.

#### Files

- `peer.py` is a Peer class that acts as a server and a client. It has a thread to listen and another
one to use RPC. 
- Each peer maintains a list of other peers who has already joined.
- The list gets updated every time a peer joins and synchronizes across all peers.
- When a peer joins the network, it asks anyone for the list, do all the computation locally,
then sends that updated list to everyone.
- That way, everyone has the latest list and is ready to be called.

#### Testing

- `pip3 install zerorpc`
- Run `peer.py` in different machines.
- You will be ask for IP to join on each machine. Default port is 9000.

## TODO

- Fix RPC calls issues in ChordServer.
- Dockerize everything
- Test over AWS
