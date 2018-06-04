import glob
import os
import sys
import subprocess

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from distutils.spawn import find_executable

proto_in_directory = "./proto"
proto_out_directory = "./tester"

protos = glob.glob(proto_in_directory + "/**/*.proto", recursive=True)


if 'PROTOC' in os.environ and os.path.exists(os.environ['PROTOC']):
    protoc = os.environ['PROTOC']
else:
    protoc = find_executable("protoc")


def generate_proto(source):
    if os.path.exists(source):
        if not os.path.exists(source):
            sys.stderr.write("Can't find required file: %s\n" % source)
            sys.exit(-1)

        if protoc is None:
            sys.stderr.write("Protocol buffers compiler 'protoc' not installed or not found.\n")
            sys.exit(-1)

        protoc_command = [protoc, "-I=" + proto_in_directory, "--python_out=" + proto_out_directory, source]
        subprocess.call(protoc_command)


class build_py(_build_py):
    def run(self):
        for proto in reversed(protos):
            generate_proto(proto)
        _build_py.run(self)


setup(
    name='proto-tester',
    packages=[
        'tester'
    ],
    install_requires=[
        'fire',
        'protobuf',
        'zmq'
    ],
    scripts=[
        'build/protobuf.py'
    ],
    cmdclass={
        'build_py': build_py
    }
)
