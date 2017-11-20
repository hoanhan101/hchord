# Chord by Nidesh and Hoanh

There are 2 versions: ChordLocal and ChordServer. Details are provided below.

## ChordLocal
ChordLocal has the main Chord logic and can be used locally, which makes it easy for testing.

#### Design
- `chord_instance.py` is a Chord Instance class, which has main Chord logic as described in the paper.
- `cons.py` has a constant key space size m.
- `node.py` is a Node class.
- `utils.py` contains helper functions.

#### Testing
- Change the key space size as you like in `const.py`.
- Change the number of nodes as you like in `chord_instance.py`.
- Run `chord_instance.py`. Tests are already written with 32 nodes and key space size equals to 16.

## ChordServer
ChordServer implements TCP networking on top of ChordLocal, using RPC.

#### Design
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
- You will be asked for IP to join. Default port is 9000.