from flask import Blueprint, flash, current_app, redirect, render_template, request, session, url_for
from authlib.integrations.flask_client import OAuth
from .db import fetch, get_conn, execute, get_error, get_error_msg
from dotenv import find_dotenv, load_dotenv
from os import environ as env

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/set_preferences', methods=['POST'])
def set_pref():
    pref_list = request.form.getlist('user_pref')
    pref_string = ','.join(pref_list)

    conn = get_conn()
    print(session['user']['id'])
    stmt = 'update users set preferences =? where id =?'

    try:
        execute(stmt, (pref_string, session['user']['id']), conn)
    except:
        print(get_error_msg())
        flash('Error setting preferences', "error")
    else:
        flash('Preferences successfully set!')
    return redirect(url_for('home'))