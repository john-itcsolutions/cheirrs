from sqlalchemy import MetaData, Table, Column, Integer, String, create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.engine import inspect

import contextlib
import time
import sys

import logging

# Create the file
# and output every level since 'DEBUG' is used
# and remove all headers in the output
# using empty format=''
logging.basicConfig(filename='models.py', level=logging.DEBUG, format='')
# Create connection string & engine
db_uri = "postgresql+psycopg2://postgres:Buddha10@10.186.165.230:5432/general"
engine = create_engine(db_uri, echo=False)

meta = MetaData()

# Performs database schema inspection
insp = reflection.Inspector.from_engine(engine)

schemas = inspector.get_schema_names()

print("The Schemas are: %s" % schemas)

with contextlib.redirect_stdout(open('models.py','w')):
    while True:
        for schema in schemas:
            print("schema: %s" % schema)
        sys.stdout.flush()
        time.sleep(1)
            for table_name in inspector.get_table_names(schema=schema):
                table = Table('table_name', meta, autoload=True, autoload_with=engine)
                primaryKeyColName = Table.primary_key.columns.values()[0].name
                print("table: %s" % table_name)
            sys.stdout.flush()
            time.sleep(1)
                for column in inspector.get_columns(table_name, schema=schema):
                    print("Column: %s" % column)
                sys.stdout.flush()
                time.sleep(1)
        