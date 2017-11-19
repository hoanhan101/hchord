# Chord

There are 2 versions: one with networking and one without networking. Both are well documented.

## ChordLocal

#### Design
- `chord_instance.py`: ChordInstance class, main Chord logic
- `cons.py`: Key space size
- `node.py`: Node class
- `utils.py`: helper functions

#### Testing
- Change the key space size as you like in `const.py`
- Change the number of nodes as you like in `chord_instance.py`
- Run `chord_instance.py`. Tests are already written.

## ChordServer

#### Design
- Using RPC, zerorpc library.

#### Testing
- `pip3 install zerorpc`
- Work in process