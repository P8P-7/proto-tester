import sys
import os
import fire
import zmq

import MessageCarrier_pb2

from google.protobuf import json_format

context = zmq.Context(1)


def send(host, port, topic, carrier_json='carrier.json'):
    print(f'Sending message from carrier.json to {host}:{port}')
    carrier = MessageCarrier_pb2.MessageCarrier()

    if not os.path.isfile(f'tester/{carrier_json}'):
        print(f'Could not find Message Carrier json file at {carrier_json}')
        return

    json_file = open(f'tester/{carrier_json}', 'r')
    json_format.Parse(json_file.read(), carrier)

    try:
        pub = context.socket(zmq.PUB)
        pub.connect(f'tcp://{host}:{port}')
    except zmq.error:
        print(f'Could not connect to {host}:{port}')
        return

    pub.send_multipart([str.encode(str(topic)), carrier.SerializeToString()])

    json_file.close()


def receive(port, topic):
    print(f'Listening for messages on *:{port} at topic {topic}')

    try:
        sub = context.socket(zmq.SUB)
        sub.bind(f'tcp://*:{port}')
        sub.setsockopt_string(zmq.SUBSCRIBE, str(topic))
    except zmq.error:
        print(f'Could not bind to *:{port} on topic {topic}')
        return

    while True:
        message = sub.recv()

        carrier = MessageCarrier_pb2.MessageCarrier()
        carrier.ParseFromString(message)
        print(json_format.MessageToJson(carrier))


def main(argv):
    fire.Fire()


if __name__ == "__main__":
    main(sys.argv)
