# coding: utf-8
import datetime
from core import tts

def handle(mic, comamnd):
    now = datetime.datetime.now()
    response = "Bây giờ là %d giờ %d phút" % (now.hour, now.minute)
    tts.espeak_tts(response)

def isMatch(command):
    return command == u"MẤY GIỜ RỒI" or command == "THOWFI GIAN"