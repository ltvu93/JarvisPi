# coding: utf-8
import time
import re
import threading
from datetime import datetime

def set_alarm(mic, hour, minute):
    mic.get_tts().speak("ĐẶT BÁO THỨC ")
    while True:
        currentHour = datetime.now().hour
        currentMinute = datetime.now().minute
        if currentHour == int(hour) and currentMinute == int(minute):
            mic.get_tts().speak_mp3("/home/pi/Music/4b896ff9151263672609e9cb9cc04c00.mp3")
            break
        else:
            print "Running..."
            time.sleep(10)

def handle(mic, command):
    hour = -1
    minute = -1
    matchObj = re.match(ur"ĐẶT BÁO THỨC LÚC (\d|1[\d]|2[0-3]) GIỜ (\d|[0-5][\d]) PHÚT", command, re.M|re.I)
    if matchObj:
        hour = matchObj.group(1).encode("utf-8")
        minute = matchObj.group(2).encode("utf-8")
    else:
        matchObj = re.match(ur"ĐẶT BÁO THỨC LÚC (\d|1[\d]|2[0-3]) GIỜ", command, re.M|re.I)
        if matchObj:
            hour = matchObj.group(1).encode("utf-8")
            minute = 0
        else:
            mic.get_tts().speak("Thời gian bạn đặt chưa đúng")
            return

    currentHour = datetime.now().hour
    currentMinute = datetime.now().minute

    if hour < currentHour or (hour == currentHour and minute < currentMinute):
        mic.get_tts().speak("Thời gian bạn đặt chưa đúng")
        return

    try:
        t=threading.Thread(target=set_alarm, args=(mic, hour, minute,))
        t.setDaemon(True)
        t.start()
    except:
        print "Error: unable to start thread"

def isMatch(command):
    return bool(re.search(ur"\bBÁO THỨC\b", command, re.IGNORECASE))
