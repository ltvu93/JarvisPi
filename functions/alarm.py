# coding: utf-8
import time
import re
import thread
from datetime import datetime 
from core import off_tts
from core import text2num

def set_alarm(hour, minute):
    while True:
        currentHour = datetime.now().hour
        currentMinute = datetime.now().minute
        if currentHour == hour and currentMinute == minute:
            print "Play ALARM"
            break
        else:
            time.sleep(10)

def handle(mic, command):
    time_alarm_str = (command.split("LÚC"))[1].strip()
    hour_str = (time_alarm_str.split("GIỜ"))[0].strip()
    exist_str = (time_alarm_str.split("GIỜ"))[1].strip()
    hour = str(hour_str)
    minute_str = (exist_str.split("PHÚT"))[0].strip()
    minute = str(minute_str)

    currentHour = datetime.now().hour
    currentMinute = datetime.now().minute

    if hour < currentHour or (hour == currentHour and minute < currentMinute):
        print "Thời gian bạn đặt chưa đúng"
        return

    try:
        t=threading.Thread(target=set_alarm, args=(hour, minute,))
        t.setDaemon(True)
        t.start()
    except:
        print "Error: unable to start thread"

def isMatch(command):else:
		return text_to_num_1(text)
    return bool(re.search(r"\bBÁO THỨC\b", command, re.IGNORECASE))
