from flask import Blueprint, flash, current_app, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from authlib.integrations.flask_client import OAuth
from .db import fetch, get_conn, execute, get_error, get_error_msg
from dotenv import find_dotenv, load_dotenv
from os import environ as env
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

oauth = OAuth(current_app)

bp = Blueprint('auth', __name__, url_prefix='/')

@bp.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        err = None

        if not email:
            err = 'E-Mail is required'
        elif not username:
            err = 'Username is required'
        elif not password:
            err = 'Password is required'

        conn = get_conn()

        if err is None:
            stmt = 'insert into users(username, email, password) values( ?, ?, ?)'
            password = generate_password_hash(password)
            try:
                execute(stmt, (username, email, password), conn)
            except:
                e = get_error()
                if e == '23505':
                    err = 'User already exists'
                print(get_error_msg())
                flash(err, "error")
            else:
                flash('Successfuly signed up!')
                return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_conn()
        err = None
        user = None
        stmt = "select * from users where email =?"

        try:
            user = fetch(stmt, username, conn)
        except:
            print(get_error_msg())

        if (user is False) or (not check_password_hash(user['PASSWORD'], password)):
            err = 'Incorrect username or password'
        

        if err is None:
            session.clear()
            session['user'] = { 'id': user['ID'], 'username': user['USERNAME'], 'email': user['EMAIL'], 'preferences': user['PREFERENCES']}
            flash("Successfully logged in!")
            return redirect(url_for('home'))
        
        flash(err, "error")
    return render_template('auth/login.html')

@bp.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('auth/success.html')

@bp.route('/google/')
def google():
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=env.get('GOOGLE_CLIENT_ID'),
        client_secret=env.get('GOOGLE_CLIENT_SECRET'),
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    # print(url_for('auth.success', _external=True))
    return oauth.google.authorize_redirect(url_for('auth.callback', _external=True))

@bp.route('/callback')
def callback():
    token = oauth.google.authorize_access_token()
    email = token["userinfo"]["email"]
    username = token["userinfo"]["name"]
    user = dict()
    user["email"] = email
    user["username"] = username
    res = None

    conn = get_conn()
    stmt = 'select * from users where email =?'

    try:
            res = fetch(stmt, email, conn)
    except:
        print(get_error_msg())

    if res is False:
        stmt = 'insert into users(username, email, password) values( ?, ?, ?);'

        try:
            execute(stmt, (username, email, ''), conn)
        except:
            e = get_error()
            if e != '23505':
                print(get_error_msg())

        finally:
            stmt = 'select * from users where email =?'
            try:
                res = fetch(stmt, email, conn)
            except:
                print(get_error_msg())

    id = res['ID']
    preferences = res['PREFERENCES']
    user["id"] = id
    user["preferences"] = preferences
    session["user"] = user
    flash("Successfully logged in!")
    return redirect(url_for('home'))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))