import click
import ibm_db

from flask import current_app, g

def get_conn():
    if 'conn' not in g:
        g.conn = ibm_db.connect(current_app.config.get('CONNECTION_STRING'), '', '')
    return g.conn

def init_db():
    conn = get_conn()

    with current_app.open_resource('schema.sql') as f:
        ibm_db.exec_immediate(conn, f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Database initialized')

def init_app(app):
    app.teardown_appcontext(close)
    app.cli.add_command(init_db_command)

def execute(sql, args, conn):
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt, args)

def fetch(sql, args, conn):
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt, args)
    res = ibm_db.fetch_both(stmt)
    print(res)
    return res

def close(e=None):
    conn = g.pop('conn', None)

    if conn is not None:
        ibm_db.close(conn)