"""main boi"""
import json
import time
import sched
import datetime
import operator
import logging
import pyttsx3
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from notifications import latest_notifications, alarm_report

FORMAT = '%(levelname)s:%(asctime)s:%(message)s'
logging.basicConfig(filename="pysys.log", level=logging.INFO, format=FORMAT)
# setup the logs file with correct formatting

with open('config.json', 'r') as f:
    config = json.load(f)
Display = config["Display"]
Settings = config['Settings']
# load the config file for customisation

s = sched.scheduler(time.time, time.sleep)
app = Flask(__name__)
engine = pyttsx3.init()
notifications = latest_notifications()
alarms = []
sched_queue = []
REFRESH = True
# declare variables

@app.route('/')
@app.route('/index')
def index():
    """The main function of the program, it has no arguments but calls the
    other functions within to create and remove alarms and notifications asynchronously
    and returns a webpage with all the processed information displayed"""
    s.run(blocking=False)

    if delete_notifications():
        return redirect('/index')
    if delete_alarms():
        return redirect('/index')

    global REFRESH
    if REFRESH:
        s.enter(int(Settings['update_rate']), 1, update_notifications)
        REFRESH = False

    if request.args.get('alarm') and request.args.get("two"):
        new_alarm = add_alarm(request.args.get('alarm'), request.args.get('two'),
                              request.args.get('news'), request.args.get('weather'))
        if new_alarm == 'alarm time set in the past':
            logging.info(new_alarm)
            return redirect('/index')
        elif new_alarm == 'alarm name already in use':
            logging.info(new_alarm)
            return redirect('/index')
        else:
            delay = (new_alarm['alarm'] - datetime.datetime.now()).total_seconds()
            logging.info("delay until alarm activation: " + str(delay))
            sched_queue.append(s.enter(delay, 1, announce, (alarm_report(new_alarm),)))
            new_alarm['sched'] = sched_queue[-1]
            alarms.sort(key=operator.itemgetter('alarm'))
            alarms.append(new_alarm)
            alarms.sort(key=operator.itemgetter('alarm'))
            logging.info(new_alarm['title'] + " added to alarms")
            return redirect('/index')
            # add alarm to schedule and alarms list
    elif request.args.get('two') and not request.args.get("alarm"):
        return redirect('/index')

    return render_template('index.html', alarms=alarms, image=Display['image'],
                           title=Display['title'], notifications=notifications)


def delete_notifications():
    """This function is called when an event happens on the webpage, and checks every
    notification and if it needs deleting from the main notifications list"""
    if notifications:
        for item in notifications:
            if request.args.get('notif') == item['title']:
                logging.info('notification ' + item['title'] + ' deleted')
                notifications.remove(item)
                return True
    return False
    # remove notifications if x clicked


def delete_alarms():
    """This function is called when an event happens on the webpage, and checks every
    alarm and if it needs deleting from the main alarms list, and removes the relavent scheduled event """
    for alarm in alarms:
        if request.args.get('alarm_item') == alarm['title']:
            try:
                s.cancel(alarm['sched'])
                logging.info("scheduling removed")
            except:
                logging.info("scheduling already removed")
            alarms.remove(alarm)
            logging.info('alarm deleted')
            return True
    return False
    # remove alarms if x clicked


def update_notifications():
    """This function is called periodically based on config settings to update all notifications"""
    notifications.clear()
    notifications.extend(latest_notifications())
    logging.info('notifications updated')
    global refresh
    refresh = True
    # update notifications at a set interval


def add_alarm(alarm_arg, alarm_title, news, weather):
    """This function takes alarm_arg, alarm_title, news, weather as inputs from the webpage and processes
    them to see if proper inputs were given and  an alarm based off the inputs can be created
    without clashing with other alarms and it returns a dictionary storing information of an alarm"""
    alarm_time = datetime.datetime(int(alarm_arg[0:4]), int(alarm_arg[5:7]), int(alarm_arg[8:10]),
                                   int(alarm_arg[11:13]), int(alarm_arg[14:16]))
    # change string of time into datetime year/month/day/hour/minute

    alarm_exists = False
    if alarm_time > datetime.datetime.now():
        for alarm in alarms:
            alarm_exists = True
            if alarm_title != alarm['title']:
                alarm_exists = False
            # if two and alarm filled, check all alarms make sure no names conflict

        if alarm_exists:
            return 'alarm name already in use'
        return alarm_content(alarm_title, alarm_time, news, weather)
        # create the content of the alarm
    return 'alarm time set in the past'


def alarm_content(alarm_title, alarm_time, news, weather):
    """takes inputs alarm_title, alarm_time, news, weather from the add_alarm
    function and puts them together into a dictionary to be returned as an alarm"""
    alarm = {'title': alarm_title, 'alarm': alarm_time,
             'content': '', 'news': False, 'weather': False, 'sched': None}
    content_string = 'Alarm to ring on ' + str(alarm_time).replace('-', '/').replace(' ', ' at ')
    if news or weather:
        content_string += ' with the following announcements:'
        if news:
            content_string += ' News,'
            alarm['news'] = True
        if weather:
            content_string += ' Weather'
            alarm['weather'] = True
    alarm['content'] = content_string
    return alarm


def announce(announcement):
    """Takes announcement as string to be outputted when an alarm goes off"""
    try:
        engine.endLoop()
    except:
        pass
    engine.say(announcement)
    engine.runAndWait()
    logging.info("announcement made")


if __name__ == '__main__':
    app.run()
