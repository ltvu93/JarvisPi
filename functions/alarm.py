# coding: utf-8
import time
import re
import threading
from core import tts
from datetime import datetime

def set_alarm(mic, hour, minute):
    tts.speak_wav("dat_bao_thuc_thanh_cong.wav", )
    while True:
        currentHour = datetime.now().hour
        currentMinute = datetime.now().minute
        if currentHour == int(hour) and currentMinute == int(minute):
            #choose WAV
            #print "ALARM"
            #mic.get_tts().speak_mp3("/home/pi/Music/4b896ff9151263672609e9cb9cc04c00.mp3")
            break
        else:
            print "Running..."
            time.sleep(10)

def handle(mic, command, profile):
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
            tts.speak_wav("thoi_gian_ban_dat_chua_dung.wav")
            return

    currentHour = datetime.now().hour
    currentMinute = datetime.now().minute

    if hour < currentHour or (hour == currentHour and minute < currentMinute):
        tts.speak_wav("thoi_gian_ban_dat_chua_dung.wav")
        return

    try:
        t=threading.Thread(target=set_alarm, args=(mic, hour, minute,))
        t.setDaemon(True)
        t.start()
    except:
        print "Error: unable to start thread"

def isMatch(command):
    return bool(re.search(ur"\bBÁO THỨC\b", command, re.IGNORECASE))
