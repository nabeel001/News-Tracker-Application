from flask import Flask, flash, redirect, render_template, request, url_for
from os import environ
import ibm_db

CONNECTION_STRING = environ.get('CONNECTION_STRING');
SECRET_KEY = environ.get('SECRET_KEY');

app = Flask(__name__)

conn = ibm_db.connect(CONNECTION_STRING, "", "")
app.secret_key = SECRET_KEY

@app.route("/")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/adduser',methods = ['POST', 'GET'])
def adduser():
    if request.method == 'POST':
        roll_no = request.form['roll_no']
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['pwd']

        sql = "SELECT * FROM users WHERE roll_no =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,roll_no)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            flash("This Account already exists, Login Directly...")
        else:
            insert_sql = "INSERT INTO users VALUES (?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, roll_no)
            ibm_db.bind_param(prep_stmt, 2, name)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, pwd)
            ibm_db.execute(prep_stmt)
            flash("User Registered Successfully")
        return redirect(url_for('login'))

@app.route('/auth',methods = ['POST', 'GET'])
def auth():
    if request.method == 'POST':
        roll_no = request.form['roll_no']
        pwd = request.form['pwd']

        sql = "SELECT * FROM users WHERE roll_no =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,roll_no)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

    if (account and account['PWD'] == pwd):
        flash("Login Successful")
        return redirect(url_for('home'))
    else:
        flash("Incorrect Username or Password","error")
        return render_template('login.html')

if __name__ == '__main__':
    app.run()