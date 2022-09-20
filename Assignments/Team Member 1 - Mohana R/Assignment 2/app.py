from flask import Flask, render_template, request
import sqlite3 

app = Flask(__name__)
db_locale = 'users.db'


@app.route('/', methods=['GET', 'POST'])
@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        details = (
            request.form['uname'],
            request.form['mailid'],
            request.form['passw']
        )
        user_mail=request.form['mailid']
        print(details)
        insert_record(details)
        return render_template('home.html',user_mail=user_mail)


@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        return render_template('signin.html')
    else:
        details = (
            request.form['mailid'],
            request.form['passw']
        )
        user_mail =  request.form['mailid']
        print(details)
        if query_db(details) is None:
            return render_template('retry.html')
        else:
            return render_template('home.html',user_mail=user_mail)

@app.route('/viewusers')
def view_users():
    user_data = display()
    return render_template('viewusers.html',user_data=user_data)
    
@app.route('/delete_user/<u_mail>')
def delete_user(u_mail):
    delete_record(u_mail)
    return render_template('signup.html')

    
def delete_record(u_mail):
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    user_mail = (u_mail,)
    sql_delete_string = 'DELETE FROM auth WHERE email == (?)'
    c.execute(sql_delete_string,user_mail)
    connie.commit()
    connie.close()
    

@app.route('/reset_pass/<u_mail>', methods=['GET', 'POST'])
def reset_pass(u_mail):
    if request.method == 'GET':
        return render_template('reset_pass.html',user_mail=u_mail)
    else:
        new_p = request.form['newp']
        print(new_p)
        update_record(u_mail,new_p)
        return render_template('signin.html')



def update_record(u_mail,new_p):
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    details = (new_p,u_mail)
    sql_update_string = 'UPDATE auth SET pass = (?) WHERE email == (?)'
    c.execute(sql_update_string,details)
    connie.commit()
    connie.close()


def query_db(details):
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    sql_select_string = 'SELECT name FROM auth WHERE exists' \
                        '(SELECT * FROM auth ' \
                        'WHERE auth.email == (?) AND auth.pass == (?))'
    c.execute(sql_select_string, details)
    result = c.fetchone()
    print(result)
    if result is None:
        return None
    else:
        return result


def insert_record(details):
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    sql_insert_string = 'INSERT INTO auth (name, email, pass) VALUES (?, ?, ?)'
    c.execute(sql_insert_string, details)
    connie.commit()
    connie.close()


def display():
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    c.execute("""
    SELECT * FROM auth
    """)
    result = c.fetchall()
    return result


if __name__ == '__main__':
    app.run()

