from sqlalchemy import *
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
db_uri = "postgresql+psycopg2://postgres:Buddha10@postgresql:5432/general"
db = create_engine(db_uri, echo=False)

meta = MetaData()

# Performs database schema inspection
insp = Inspector.from_engine(db)

schemas = insp.get_schema_names()

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
                