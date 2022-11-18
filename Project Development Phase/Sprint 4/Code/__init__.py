from os import environ as env
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, url_for, session, request, jsonify

import requests
from ip2geotools.databases.noncommercial import DbIpCity

from .articles import businessArticles, entArticles, get_news_source, healthArticles, prefArticles, publishedArticles, publishedArticles2, randomArticles, scienceArticles, sportArticles, techArticles, topHeadlines, get_sources_and_domains

def create_app():
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)

    app = Flask(__name__)
    app.config['SECRET_KEY'] = env.get("SECRET_KEY")

    def get_ip_country():
        ip_address_res = requests.get('https://api64.ipify.org?format=json').json()
        ip_address = ip_address_res["ip"]
        response = DbIpCity.get(ip_address, api_key='free')
        return response.country    

    @app.route('/',methods=['POST','GET'])
    def home():
        if request.method == 'POST':
            keyword = request.form["keyword"]
            articles = publishedArticles2(keyword)
            return render_template('home.html',articles=articles)
        else:
            country = get_ip_country()
            if session.get('user') != None and session['user']['preferences'] != None:
                pref_list = session['user']['preferences'].split(',')
                articles = prefArticles(pref_list)
            else:
                articles = publishedArticles(country)
            return render_template('home.html',articles=articles,country=country)


    @app.route('/headlines')
    def headlines():
        headlines = topHeadlines()

        return  render_template('headlines.html', headlines = headlines)

    @app.route('/articles')
    def articles():
        random = randomArticles()

        return  render_template('articles.html', random = random)

    @app.route('/sources')
    def sources():
        newsSource = get_news_source()

        return  render_template('sources.html', newsSource = newsSource)

    @app.route('/category/business')
    def business():
        sources = businessArticles()

        return  render_template('business.html', sources = sources)

    @app.route('/category/tech')
    def tech():
        sources = techArticles()

        return  render_template('tech.html', sources = sources)

    @app.route('/category/entertainment')
    def entertainment():
        sources = entArticles()

        return  render_template('entertainment.html', sources = sources)

    @app.route('/category/science')
    def science():
        sources = scienceArticles()

        return  render_template('science.html', sources = sources)

    @app.route('/category/sports')
    def sports():
        sources = sportArticles()

        return  render_template('sport.html', sources = sources)

    @app.route('/category/health')
    def health():
        sources = healthArticles()

        return  render_template('health.html', sources = sources)

    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)

    from . import user
    app.register_blueprint(user.bp)

    # from . import views

    return app