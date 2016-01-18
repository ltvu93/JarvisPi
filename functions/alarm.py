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
    hour = -1
    minute = -1
    matchObj = re.match(ur"ĐẶT BÁO THỨC LÚC (\d|1[\d]|2[0-3]) GIỜ (\d|[0-5][\d]) PHÚT", command, re.M|re.I)
    if matchObj:
        hour = matchObj1.group(1).encode("utf-8")
        minute = matchObj1.group(2).encode("utf-8")
    else:
        matchObj1 = re.match(ur"ĐẶT BÁO THỨC LÚC (\d|1[\d]|2[0-3]) GIỜ", command, re.M|re.I)
        if matchObj1:
            hour = matchObj1.group(1).encode("utf-8")
            minute = 0
        else:
            print "Thời gian bạn đặt chưa đúng"
            return

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
