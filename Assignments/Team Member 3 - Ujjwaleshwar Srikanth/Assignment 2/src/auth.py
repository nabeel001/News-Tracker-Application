import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from src.db import fetch, get_conn, execute
import ibm_db
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        rollnumber = int(request.form['rollnumber'])
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        conn = get_conn()
        err = None

        if not rollnumber:
            err = 'Rollnumber is required'
        elif not username:
            err = 'Username is required'
        elif not password:
            err = 'Password is required'

        if err is None:
            stmt = 'insert into users values( ? , ? , ? , ?);'
            password = generate_password_hash(password)
            try:
                execute(stmt, (rollnumber, email, username, password), conn)
            except:
                e = ibm_db.stmt_error()
                if e == '23505':
                    err = 'User already exists'
                print(ibm_db.stmt_errormsg())
            else:
                return redirect(url_for("auth.login"))
        
        flash(err)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_conn()
        err = None
        user = None
        stmt = 'select * from users where username = \''+username + '\';'

        try:
            res = ibm_db.exec_immediate(conn, stmt)
            user = ibm_db.fetch_both(res)    
            # user = fetch(stmt, (username), conn)        
        except:
            print(ibm_db.stmt_errormsg())
        # print(user)

        if user is None:
            err = 'Incorrect username or password'
        elif not check_password_hash(user['PASSWORD'], password):
            err = 'Incorrect username or password'

        if err is None:
            session.clear()
            session['user_id'] = user['ROLLNUMBER']
            return redirect(url_for('welcome'))

        flash(err)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        conn = get_conn()
        g.user = ibm_db.exec_immediate(conn, 'select * from users where rollnumber = ' + str(user_id) + ';')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view