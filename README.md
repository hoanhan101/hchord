# Chord by Nidesh and Hoanh

There are 2 versions: ChordLocal and ChordServer. Details are provided below.

## ChordLocal
ChordLocal has the main Chord logic and can be used locally, which makes it easy for testing.

#### Design
- `chord_instance.py` is a Chord Instance class, which has main Chord logic as described in the paper.
- `const.py` has a constant key space size m.
- `node.py` is a Node class.
- `utils.py` contains helper functions.

#### Testing
- Change the key space size as you like in `const.py`.
- Change the number of nodes as you like in `chord_instance.py`.
- Run `chord_instance.py`. Tests are already written with 32 nodes and key space size equals to 16.

## ChordServer
ChordServer implements TCP networking on top of ChordLocal, using RPC. We chose to use
 [zerorpc](http://www.zerorpc.io "zerorpc's Homepage") module for this purpose.

#### Design
- `peer.py` is a Peer class that acts as a server and a client. It has a thread to listen and another
one to use RPC. The server starts listening at the default port (9000) which can be modified in `const.py`.
- The client thread runs and asks the user which IP and port to connect to. The client then tries to connect
 to the given TCP address. If the client fails to find the server with that address in the network within 10
  seconds, then it will create a new ring with the server as the node.
- If the client is successful in connecting to a peer's server, then it will call its join function to that peer.
 Finger tables will be updated and a new node will be attached to our ring. 
- The algorithms for the joining and updated finger tables are discussed in detail in the paper.

#### Testing
The chord implementation with networking is located in the [ChordServer](../blob/master/ChordServer/) folder.

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