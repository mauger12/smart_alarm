"""The news_report function uses the newsapi API to get
the top headlines in the news to be used in the __main__ module"""
from flask import Markup
import requests


def top_headlines(api_key, filters):
    """Takes an API key and a list of filters and returns the top 5
    headlines containing the filters to be displayed as notifications"""
    base_url = "https://newsapi.org/v2/top-headlines?"
    country = "gb"
    complete_url = base_url + "country=" + country + "&apiKey=" + api_key
    response = requests.get(complete_url)
    news_dict = response.json()
    articles = news_dict["articles"]
    headlines = []
    for article in articles:
        for keyword in filters:
            if len(headlines) < 5 and keyword in article['title']:
                headlines.append({'title': article['title'],
                                  'content': Markup('<a href = \'' + article['url'] +'\'> '+
                                                    str(article['source']['name']) + ' </a>')})
    return headlines


def news_alarm(api_key, filters):
    """Takes an API key and a list of filters and returns a report on
    the top 3 headlines with the filters to be used for announcements"""
    base_url = "https://newsapi.org/v2/top-headlines?"
    country = "gb"
    complete_url = base_url + "country=" + country + "&apiKey=" + api_key
    response = requests.get(complete_url)
    news_dict = response.json()
    articles = news_dict["articles"]
    no_headlines = 0
    report = "Today's top 3 headlines: "
    for article in articles:
        for keyword in filters:
            if no_headlines < 3 and keyword in article['title']:
                report += article['title'] + '. '
                no_headlines += 1
    return report
