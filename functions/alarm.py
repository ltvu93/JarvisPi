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
            print "Play alarm"
            break
        else:
            time.sleep(10)

def handle(mic, command):
    time_alarm_str = (command.split("LÚC"))[1].strip()
    hour_str = (time_alarm_str.split("GIỜ"))[0].strip()
    exist_str = (time_alarm_str.split("GIỜ"))[1].strip()
    hour = text_to_num_2(hour_str)
    minute_str = (exist_str.split("PHÚT"))[0].strip()
    minute = text_to_num_2(minute_str)
    try:
        t=threading.Thread(target=set_alarm, args=(hour, minute,))
        t.daemon = True  # set thread to daemon ('ok' won't be printed in this case)
        t.start()
    except:
        print "Error: unable to start thread"

def isMatch(command):
    return bool(re.search(r"\bBÁO THỨC\b", command, re.IGNORECASE))
