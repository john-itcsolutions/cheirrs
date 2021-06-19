#!/bin/bash

virtualenv -p `which python3` venv

source venv/bin/activate

pip install -r requirements.txt

export PYTHONPATH="$PYTHONPATH:$PWD/grpc_adenine/stubs/"

python3 grpc_adenine/server.py
