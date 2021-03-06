from sqlalchemy_wrapper import SQLAlchemy
from decouple import config
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey
from sqlalchemy.ext.automap import automap_base

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

from charmhelpers.core.hookenv import (
    Hooks, config, relation_set, relation_get,
    local_unit, related_units, remote_unit)

hooks = Hooks()
hook = hooks.hook

@hook
def db_relation_joined():
    relation_set('database', config('general'))  # Explicit database name
    relation_set('roles', 'reporting,standard')  # DB roles required
    relation_set('extensions', 'postgis,osm2pgrouting') # Get PostGIS
@hook('db-relation-changed', 'db-relation-departed')
def db_relation_changed():
    # Rather than try to merge in just this particular database
    # connection that triggered the hook into our existing connections,
    # it is easier to iterate over all active related databases and
    # reset the entire list of connections.
    conn_str_tmpl = "dbname={dbname} user={user} host={host} port={port}"
    master_conn_str = None
    slave_conn_strs = []
    for db_unit in related_units():
        if relation_get('database', db_unit) != config('database'):
            continue  # Not yet acknowledged requested database name.

        allowed_units = relation_get('allowed-units') or ''  # May be None
        if local_unit() not in allowed_units.split():
            continue  # Not yet authorized.

        conn_str = conn_str_tmpl.format(**relation_get(unit=db_unit)
        remote_state = relation_get('state', db_unit)

        if remote_state == 'standalone' and len(active_db_units) == 1:
            master_conn_str = conn_str
        elif relation_state == 'master':
            master_conn_str = conn_str
        elif relation_state == 'hot standby':
            slave_conn_strs.append(conn_str)

    update_my_db_config(master=master_conn_str, slaves=slave_conn_strs)

if __name__ == '__init__':
    hooks.execute(sys.argv)