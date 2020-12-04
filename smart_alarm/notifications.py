"""The notifications module takes the outputs from the API's and processes
it into simple outputs for the __main__ module to easily process"""
import datetime
import json
from weather_report import current_weather
from covid_report import weekly_cases_update, total_cases_update
from news_report import top_headlines, news_alarm

with open('config.json', 'r') as f:
    config = json.load(f)
keys = config["API-keys"]
Settings = config["Settings"]


def latest_notifications():
    """Taking no arguments, this function the current weather, covid data and top headlines
    and is returned as a list of dictionaries with each dictionary storing a notification"""
    notifications = [{'title': 'Weather on ' + str(datetime.datetime.now().day) + '/' + str(
        datetime.datetime.now().month) + '/' + str(datetime.datetime.now().year) + ' at ' + str(
        datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                      'content': current_weather(Settings['city'], Settings['units'], keys['weather'])},
                     {'title': 'Corona update in ' + Settings['city'], 'content': str(weekly_cases_update(
                         Settings['city'])) + ' New cases in the past week. Total cases are ' + total_cases_update(
                         Settings['city'])}]
    notifications.extend(top_headlines(keys['news'], Settings['news_filters']))
    return notifications


def alarm_report(alarm):
    """taking an alarm in the form of a dictionary, it looks at which announcements need
    to be outputted when the alarm goes off, and returns them as a single report"""
    report = str(alarm['title']) + ' at time: ' + str(alarm['alarm'])
    if alarm['news'] or alarm['weather']:
        if alarm['news']:
            report += news_alarm(keys['news'], Settings['news_filters']) + '.'
        if alarm['weather']:
            report += ' ' + current_weather(Settings['city'], Settings['units'], keys['weather'])
    return report
