import click
from os import environ as env
import ibm_db
from flask import current_app, g
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

def get_conn():
    if 'conn' not in g:
        g.conn = ibm_db.connect(env.get("CONNECTION_STRING"), '', '')
    return g.conn

def init_db():
    conn = get_conn()
    with current_app.open_resource('schema.sql') as f:
        ibm_db.exec_immediate(conn, f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    print('hello')
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
    # print(args)
    ibm_db.bind_param(stmt, 1, args)
    # ibm_db.execute(stmt, args)
    ibm_db.execute(stmt)
    res = ibm_db.fetch_assoc(stmt)
    return res

def get_error():
    return ibm_db.stmt_error()

def get_error_msg():
    return ibm_db.stmt_errormsg()

def close(e=None):
    conn = g.pop('conn', None)
    if conn is not None:
        ibm_db.close(conn)

