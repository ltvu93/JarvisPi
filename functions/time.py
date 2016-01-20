# coding: utf-8
import datetime
from core import converter

def handle(mic, comamnd, profile):
    now = datetime.datetime.now()
    if now.minute == 0:
        response = "Bây giờ là %d giờ" % (now.hour)
    else:
        response = "Bây giờ là %d giờ %d phút" % (now.hour, now.minute)
    mic.speak(response)

def isMatch(command):
    return command == u"MẤY GIỜ RỒI" or command == "THOWFI GIAN"
