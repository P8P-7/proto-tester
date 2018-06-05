# Proto Tester
## How To Use
#### Generate protobufs
```bash
python setup.py build_py
```
#### Send A Message Carrier
1. Update JSON file
2. 
```
python tester/tester.py send <host> <port> <topic> <path to json file>
```
#### Receive A Message Carrier
```
python tester/tester.py receive <host> <port> <topic>
```