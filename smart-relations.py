import sys
from charmhelpers.core.hookenv import (
    Hooks, config, relation_set, relation_get,
    local_unit, related_units, remote_unit)

hooks = Hooks()
hook = hooks.hook

@hook
def db_relation_joined():
    relation_set('database', config('general'))  # Explicit database name
    relation_set('roles', 'reporting,standard')  # DB roles required
    relation_set('extensions', 'postgis,pgroute' ) # Get PostGIS
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

if __name__ == '__main__':
    hooks.execute(sys.argv)