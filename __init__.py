from sqlalchemy import *
from sqlalchemy.engine import reflection, inspect

import contextlib
import time
import sys

import logging

from charmhelpers.core.hookenv import (
    Hooks, config, relation_set, relation_get,
    local_unit, related_units, remote_unit)

class BaseModel(db.Model):

    def before_save(self, *args, **kwargs):
        pass

    def after_save(self, *args, **kwargs):
        pass

    def save(self, commit=True):
        self.before_save()
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

        self.after_save()


    def before_update(self, *args, **kwargs):
        pass

    def after_update(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        self.before_update(*args, **kwargs)
        db.session.commit()
        self.after_update(*args, **kwargs)

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()

    @classmethod
    def eager(cls, *args):
        cols = [orm.joinedload(arg) for arg in args]
        return cls.query.options(*cols)

    @classmethod
    def before_bulk_create(cls, iterable, *args, **kwargs):
        pass

    @classmethod
    def after_bulk_create(cls, model_objs, *args, **kwargs):
        pass


    @classmethod
    def bulk_create(cls, iterable, *args, **kwargs):
        cls.before_bulk_create(iterable, *args, **kwargs)
        model_objs = []
        for data in iterable:
            if not isinstance(data, cls):
                data = cls(**data)
            model_objs.append(data)

        db.session.bulk_save_objects(model_objs)
        if kwargs.get('commit', True) is True:
            db.session.commit()
        cls.after_bulk_create(model_objs, *args, **kwargs)
        return model_objs


    @classmethod
    def bulk_create_or_none(cls, iterable, *args, **kwargs):
        try:
            return cls.bulk_create(iterable, *args, **kwargs)
        except exc.IntegrityError as e:
            db.session.rollback()
            return None

# Create the models.py file
# and output every level since 'DEBUG' is used
# and remove all headers in the output
# using empty format=''
logging.basicConfig(filename='models.py', level=logging.DEBUG, format='')

# Create database connection string & engine
db_uri = "postgresql+psycopg2://postgres:Buddha10@postgresql:5432/general"

db = create_engine(db_uri, echo=False)

meta = MetaData()

# Performs database schema inspection
insp = Inspector.from_engine(db)

schemas = insp.get_schema_names()

print("The Schemas are: %s" % schemas)

# At this stage we are still developing this __init__.py file
# to produce a complete database connection and set of Models 
# for SQLAlchemy to use, prior to the running of server.py.
# This initialisation process should only happen once per 
# application (re-)start. We use the logging module in python to 
# print to a file. Extending the BaseModel Class above shortens the 
# coding process considerably.

for schema in schemas:
    logging.debug('schema: %s' % schema)

    for table_name in insp.get_table_names(schema=schema):
        table = Table('table_name', meta, autoload=True, autoload_with=engine)
        primaryKeyColName = Table.primary_key.columns.values()[0].name
        print("Primary key Col Name is %s" % primaryKeyColName)
        logging.debug('table: %s' % table_name)
    
        for column in insp.get_columns(table_name, schema=schema):
            logging.debug('Column: %s' % column)

hooks = Hooks()
hook = hooks.hook

@hook
def db_relation_joined():
    relation_set('database', config('general'))  # Explicit database name
    relation_set('roles', 'reporting,standard')  # DB roles required
    relation_set('extensions', 'postgis,osm2pgrouting' ) # Get PostGIS
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

                