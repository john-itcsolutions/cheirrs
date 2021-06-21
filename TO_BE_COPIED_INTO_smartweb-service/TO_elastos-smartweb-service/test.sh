#!/bin/bash

# Run pytest
virtualenv -p `which python3` venv
source venv/bin/activate
pip install -q -r requirements.txt
SHARED_SECRET_ADENINE=7XDnFBdHafpPyIC4nrtuJ5EUYVqdEKjW DB_NAME=haus DB_PORT=5432 py.test --disable-pytest-warnings -v -xs grpc_adenine/implementations/common_test.py
DB_NAME=haus DB_PORT=5432 py.test --disable-pytest-warnings -v -xs grpc_adenine/implementations/hive_test.py
DB_NAME=haus DB_PORT=5432 py.test --disable-pytest-warnings -v -xs grpc_adenine/implementations/wallet_test.py
DB_NAME=haus DB_PORT=5432 py.test --disable-pytest-warnings -v -xs grpc_adenine/implementations/sidechain_eth_test.py
DB_NAME=haus DB_PORT=5432 py.test --disable-pytest-warnings -v -xs grpc_adenine/implementations/node_rpc_test.py

# Cleanup
deactivate

