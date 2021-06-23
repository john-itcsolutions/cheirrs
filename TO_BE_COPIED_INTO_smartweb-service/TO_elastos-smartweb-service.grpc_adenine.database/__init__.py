from sqlalchemy_wrapper import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, inspect
from sqlalchemy.ext.automap import automap_base
import psycopg2
import sys
from decouple import config
from charmhelpers.core.hookenv  import (
    Hooks, config, relation_set, relation_get,
    local_unit, related_units, remote_unit)

import logging
# Set up logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Connect to the database
db_name = 'haus'
db_user = 'gmu'
db_password = 'gmu'
db_host = '10.57.133.149'
db_port = '5432'

database_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

try:
    db_engine = create_engine(database_uri)
    connection = SQLAlchemy(database_uri)
except Exception as e:
    logging.fatal(f"Error while connecting to the database: {e}")

hooks = Hooks()
hook = hooks.hook

@hook
def db_relation_joined():
    relation_set('database', 'haus')  # Explicit database name
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

        conn_str = conn_str_tmpl.format(**relation_get(unit=db_unit))
        remote_state = relation_get('state', db_unit)

        if remote_state == 'standalone' and len(db_unit) == 1:
            master_conn_str = conn_str
        elif remote_state == 'master':
            master_conn_str = conn_str
        elif remote_state == 'hot standby':
            slave_conn_strs.append(conn_str)

    update_my_db_config(master=master_conn_str, slaves=slave_conn_strs)

# Utilise metadata inspection to reflect database/schema details
meta = MetaData()
insp = inspect(db_engine)
n = 0
m = 0
l = 0
max = [[]]
mAX = 0

schemata_names = ['public', 'a_horse', 'cheirrs', 'cheirrs_oseer', 'chubba_morris', 'chubba_morris_oseer', 'convey_it', 'convey_it_oseer', 'the_general',  'the_general_oseer', 'tiger', 'tiger_data', 'topology']
for schema in schemata_names:
    n += 1
    if n > 1:
        max.append((last_schema, m))
        mAX += m
        m = 0
    for table in insp.get_table_names(schema):
        this_table = Table(table, meta)
        insp.reflect_table(this_table, None)
        m += 1
        l += 1
        print(schema, '.', this_table)
        last_schema = schema
max.append((last_schema, m))
mAX += m
print('All', n, 'schemata, with', l, 'total tables reflected')
print(str(max).replace("),", "),\n"))

print('Total tables by "max" =', mAX)
if mAX - l == 0:
    print('Totals agree!')
else:
    print('WARNING!! Totals not equal!')

if __name__ == '__main__':
    hooks.execute(sys.argv)
