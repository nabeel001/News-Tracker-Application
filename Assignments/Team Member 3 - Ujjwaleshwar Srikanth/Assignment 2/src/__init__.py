import os
from flask import Flask, redirect, render_template, url_for

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('settings.py')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/')
    @app.route('/home')
    def index():
        return redirect(url_for('auth.register'))

    @app.route('/welcome')
    def welcome():
        return render_template('welcome.html')

    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    return app