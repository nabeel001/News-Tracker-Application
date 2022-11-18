from .models import Articles
from .models import Sources
from newsapi import NewsApiClient
from os import environ as env
from dotenv import find_dotenv, load_dotenv
import requests
import json
import urllib.request,json

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

api_key=None
base_url=None
base_url_for_everything=None
base_url_top_headlines=None
base_source_list=None

def publishedArticles(country):
    api_key = env.get("API_KEY")
    url = "https://newsapi.org/v2/top-headlines?country=" + country + "&apiKey=" + api_key
    get_articles = requests.get(url).content
    all_articles = json.loads(get_articles)['articles']

    articles_results = []

    source = []
    title = []
    desc = []
    author = []
    img = []
    p_date = []
    url = []

    for i in range(len(all_articles)):
        article = all_articles[i]

        if(article['source']['name'] == 'Analytics Insight' or article['source']['name'] == 'Google News' or article['source']['name'] == 'Financial Times' or article['source']['name'] == 'MyBroadband' or article['source']['name'] == 'Sportskeeda' or article['source']['name'] == 'Ottawahospital.on.ca'):
            continue

        source.append(article['source'])
        title.append(article['title'])
        desc.append(article['description'])
        author.append(article['author'])
        img.append(article['urlToImage'])
        p_date.append(article['publishedAt'])
        url.append(article['url'])

        article_object = Articles(source, title, desc, author, img, p_date, url)

        articles_results.append(article_object)

        contents = zip(source, title, desc, author, img, p_date, url)

    return  contents


def publishedArticles2(keyw):
    newsapi = NewsApiClient(api_key= env.get("API_KEY"))

    get_articles = newsapi.get_everything(q=keyw,sources= 'cnn, reuters, cnbc, the-verge, gizmodo, the-next-web, techradar, recode, ars-technica')

    all_articles = get_articles['articles']

    articles_results = []

    source = []
    title = []
    desc = []
    author = []
    img = []
    p_date = []
    url = []

    for i in range(len(all_articles)):
        article = all_articles[i]

        source.append(article['source'])
        title.append(article['title'])
        desc.append(article['description'])
        author.append(article['author'])
        img.append(article['urlToImage'])
        p_date.append(article['publishedAt'])
        url.append(article['url'])

        article_object = Articles(source, title, desc, author, img, p_date, url)

        articles_results.append(article_object)

        contents = zip(source, title, desc, author, img, p_date, url)

    return  contents

def topHeadlines():
    newsapi = NewsApiClient(api_key= env.get("API_KEY"))

    top_headlines = newsapi.get_top_headlines(sources= 'cnn, reuters, cnbc, techcrunch, the-verge, gizmodo, the-next-web, techradar, recode, ars-technica')

    all_headlines = top_headlines['articles']

    articles_results = []

    source = []
    title = []
    desc = []
    author = []
    img = []
    p_date = []
    url = []

    for i in range(len(all_headlines)):
        headline = all_headlines[i]

        source.append(headline['source'])
        title.append(headline['title'])
        desc.append(headline['description'])
        author.append(headline['author'])
        img.append(headline['urlToImage'])
        p_date.append(headline['publishedAt'])
        url.append(headline['url'])

        article_object = Articles(source, title, desc, author, img, p_date, url)

        articles_results.append(article_object)

        contents = zip(source, title, desc, author, img, p_date, url)

    return  contents

def randomArticles():
    newsapi = NewsApiClient(api_key= env.get("API_KEY"))

    random_articles = newsapi.get_everything(sources= 'the-verge, gizmodo, the-next-web, recode, ars-technica')

    all_articles = random_articles['articles']

    articles_results = []

    source = []
    title = []
    desc = []
    author = []
    img = []
    p_date = []
    url = []

    for i in range(len(all_articles)):
        article = all_articles[i]

        source.append(article['source'])
        title.append(article['title'])
        desc.append(article['description'])
        author.append(article['author'])
        img.append(article['urlToImage'])
        p_date.append(article['publishedAt'])
        url.append(article['url'])

        article_object = Articles(source, title, desc, author, img, p_date, url)

        articles_results.append(article_object)

        contents = zip(source, title, desc, author, img, p_date, url)

    return  contents

def prefArticles(pref_list):
    newsapi = NewsApiClient(api_key= env.get("API_KEY"))
    biz = []
    tech = []
    ent = []
    sci = []
    sport = []
    health = []

    if 'Business' in pref_list:
        biz = newsapi.get_top_headlines(category='business')['articles']
    if 'Technology' in pref_list:
        tech = newsapi.get_top_headlines(category='technology')['articles']
    if 'Entertainment' in pref_list:
        ent = newsapi.get_top_headlines(category='entertainment')['articles']
    if 'Science' in pref_list:
        sci = newsapi.get_top_headlines(category='science')['articles']
    if 'Sport' in pref_list:
        sport = newsapi.get_top_headlines(category='sport')['articles']
    if 'Health' in pref_list:
        health = newsapi.get_top_headlines(category='health')['articles']

    articles = biz + tech + ent + sci + sport + health

    sorted(articles, key=lambda x: x['publishedAt'])

    results = []

    source = []
    title = []
    desc = []
    author = []
    img = []
    p_date = []
    url = []

    for i in range(len(articles)):
        article = articles[i]

        if(article['source']['name'] == 'Analytics Insight' or article['source']['name'] == 'Google News' or article['source']['name'] == 'Financial Times' or article['source']['name'] == 'MyBroadband' or article['source']['name'] == 'Sportskeeda' or article['source']['name'] == 'Ottawahospital.on.ca'):
            continue

        source.append(article['source'])
        title.append(article['title'])
        desc.append(article['description'])
        author.append(article['author'])
        img.append(article['urlToImage'])
        p_date.append(article['publishedAt'])
        url.append(article['url'])

        article_object = Articles(source, title, desc, author, img, p_date, url)

        results.append(article_object)

        contents = zip(source, title, desc, author, img, p_date, url)

    return  contents
    


def businessArticles():
    newsapi = NewsApiClient(api_key= env.get("API_KEY"))

    business_articles = newsapi.get_top_headlines(category='business')

    all_articles = business_articles['articles']

    business_articles_results = []

    source = []
    title = []
    desc = []
    author = []
    img = []
    p_date = []
    url = []

    for i in range(len(all_articles)):
        article = all_articles[i]

        if(article['source']['name'] == 'Analytics Insight' or article['source']['name'] == 'Google News' or article['source']['name'] == 'Financial Times' or article['source']['name'] == 'MyBroadband' or article['source']['name'] == 'Sportskeeda' or article['source']['name'] == 'Ottawahospital.on.ca'):
            continue

        source.append(article['source'])
        title.append(article['title'])
        desc.append(article['description'])
        author.append(article['author'])
        img.append(article['urlToImage'])
        p_date.append(article['publishedAt'])
        url.append(article['url'])

        article_object = Articles(source, title, desc, author, img, p_date, url)

        business_articles_results.append(article_object)

        contents = zip(source, title, desc, author, img, p_date, url)

    return  contents

def techArticles():
    newsapi = NewsApiClient(api_key= env.get("API_KEY"))

    tech_articles = newsapi.get_top_headlines(category='technology')

    all_articles = tech_articles['articles']

    tech_articles_results = []

    source = []
    title = []
    desc = []
    author = []
    img = []
    p_date = []
    url = []

    for i in range(len(all_articles)):
        article = all_articles[i]

        if(article['source']['name'] == 'Analytics Insight' or article['source']['name'] == 'Google News' or article['source']['name'] == 'Financial Times' or article['source']['name'] == 'MyBroadband' or article['source']['name'] == 'Sportskeeda' or article['source']['name'] == 'Ottawahospital.on.ca'):
            continue

        source.append(article['source'])
        title.append(article['title'])
        desc.append(article['description'])
        author.append(article['author'])
        img.append(article['urlToImage'])
        p_date.append(article['publishedAt'])
        url.append(article['url'])

        article_object = Articles(source, title, desc, author, img, p_date, url)

        tech_articles_results.append(article_object)

        contents = zip(source, title, desc, author, img, p_date, url)

    return  contents

def entArticles():
    newsapi = NewsApiClient(api_key= env.get("API_KEY"))

    ent_articles = newsapi.get_top_headlines(category='entertainment')

    all_articles = ent_articles['articles']

    ent_articles_results = []

    source = []
    title = []
    desc = []
    author = []
    img = []
    p_date = []
    url = []

    for i in range(len(all_articles)):
        article = all_articles[i]

        if(article['source']['name'] == 'Analytics Insight' or article['source']['name'] == 'Google News' or article['source']['name'] == 'Financial Times' or article['source']['name'] == 'MyBroadband' or article['source']['name'] == 'Sportskeeda' or article['source']['name'] == 'Ottawahospital.on.ca'):
            continue

        source.append(article['source'])
        title.append(article['title'])
        desc.append(article['description'])
        author.append(article['author'])
        img.append(article['urlToImage'])
        p_date.append(article['publishedAt'])
        url.append(article['url'])

        article_object = Articles(source, title, desc, author, img, p_date, url)

        ent_articles_results.append(article_object)

        contents = zip(source, title, desc, author, img, p_date, url)

    return  contents

def scienceArticles():
    newsapi = NewsApiClient(api_key= env.get("API_KEY"))

    science_articles = newsapi.get_top_headlines(category='science')

    all_articles = science_articles['articles']

    science_articles_results = []

    source = []
    title = []
    desc = []
    author = []
    img = []
    p_date = []
    url = []

    for i in range(len(all_articles)):
        article = all_articles[i]

        if(article['source']['name'] == 'Analytics Insight' or article['source']['name'] == 'Google News' or article['source']['name'] == 'Financial Times' or article['source']['name'] == 'MyBroadband' or article['source']['name'] == 'Sportskeeda' or article['source']['name'] == 'Ottawahospital.on.ca'):
            continue

        source.append(article['source'])
        title.append(article['title'])
        desc.append(article['description'])
        author.append(article['author'])
        img.append(article['urlToImage'])
        p_date.append(article['publishedAt'])
        url.append(article['url'])

        article_object = Articles(source, title, desc, author, img, p_date, url)

        science_articles_results.append(article_object)

        contents = zip(source, title, desc, author, img, p_date, url)

    return  contents

def sportArticles():
    newsapi = NewsApiClient(api_key= env.get("API_KEY"))

    sport_articles = newsapi.get_top_headlines(category='sports')

    all_articles = sport_articles['articles']

    sport_articles_results = []

    source = []
    title = []
    desc = []
    author = []
    img = []
    p_date = []
    url = []

    for i in range(len(all_articles)):
        article = all_articles[i]

        if(article['source']['name'] == 'Analytics Insight' or article['source']['name'] == 'Google News' or article['source']['name'] == 'Financial Times' or article['source']['name'] == 'MyBroadband' or article['source']['name'] == 'Sportskeeda' or article['source']['name'] == 'Ottawahospital.on.ca'):
            continue

        source.append(article['source'])
        title.append(article['title'])
        desc.append(article['description'])
        author.append(article['author'])
        img.append(article['urlToImage'])
        p_date.append(article['publishedAt'])
        url.append(article['url'])

        article_object = Articles(source, title, desc, author, img, p_date, url)

        sport_articles_results.append(article_object)

        contents = zip(source, title, desc, author, img, p_date, url)

    return  contents

def healthArticles():
    newsapi = NewsApiClient(api_key= env.get("API_KEY"))

    health_articles = newsapi.get_top_headlines(category='health')

    all_articles = health_articles['articles']

    health_articles_results = []

    source = []
    title = []
    desc = []
    author = []
    img = []
    p_date = []
    url = []

    for i in range(len(all_articles)):
        article = all_articles[i]

        if(article['source']['name'] == 'Analytics Insight' or article['source']['name'] == 'Google News' or article['source']['name'] == 'Financial Times' or article['source']['name'] == 'MyBroadband' or article['source']['name'] == 'Sportskeeda' or article['source']['name'] == 'Ottawahospital.on.ca'):
            continue

        source.append(article['source'])
        title.append(article['title'])
        desc.append(article['description'])
        author.append(article['author'])
        img.append(article['urlToImage'])
        p_date.append(article['publishedAt'])
        url.append(article['url'])

        article_object = Articles(source, title, desc, author, img, p_date, url)

        health_articles_results.append(article_object)

        contents = zip(source, title, desc, author, img, p_date, url)

    return  contents

def get_news_source():
  '''
  Function that gets the json response to our url request
  '''
  get_news_source_url = 'https://newsapi.org/v2/sources?apiKey=' + env.get("API_KEY")
  with urllib.request.urlopen(get_news_source_url) as url:
    get_news_source_data = url.read()
    get_news_source_response = json.loads(get_news_source_data)

    news_source_results = None

    if get_news_source_response['sources']:
      news_source_results_list = get_news_source_response['sources']
      news_source_results = process_sources(news_source_results_list)

  return news_source_results

def process_sources(source_list):
  '''
  function that process the news articles and transform them to a list of objects
  '''
  news_source_result = []
  for news_source_item in source_list:
    name = news_source_item.get('name')
    description = news_source_item.get('description')
    url = news_source_item.get('url')

    if name:
      news_source_object = Sources(name, description,url)
      news_source_result.append(news_source_object)
  return news_source_result


# helper function
def get_sources_and_domains():
    newsapi = NewsApiClient(api_key= env.get("API_KEY"))
    all_sources = newsapi.get_sources()['sources']
    sources = []
    domains = []
    for e in all_sources:
       id = e['id']
       domain = e['url'].replace("http://", "")
       domain = domain.replace("https://", "")
       domain = domain.replace("www.", "")
       slash = domain.find('/')
       if slash != -1:
        domain = domain[:slash]
        sources.append(id)
        domains.append(domain)
        sources = ", ".join(sources)
        domains = ", ".join(domains)
    return sources, domains