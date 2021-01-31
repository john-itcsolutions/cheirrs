from sqlalchemy_wrapper import SQLAlchemy
from decouple import config
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey
from sqlalchemy.ext.automap import automap_base

import contextlib
import time
import sys

import logging
# Set up logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Connect to the database
db_name = config('DB_NAME')
db_user = config('DB_USER')
db_password = config('DB_PASSWORD')
db_host = config('DB_HOST')
db_port = config('DB_PORT')

database_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

try:
    db_engine = create_engine(database_uri)
    connection = SQLAlchemy(database_uri)
except Exception as e:
    logging.fatal(f"Error while connecting to the database: {e}")

# produce our own MetaData object
metadata = MetaData(reflect=True)

metadata.reflect(db_engine)

Base = automap_base(metadata=metadata)

Base.prepare()