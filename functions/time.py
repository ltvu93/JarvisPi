# coding: utf-8
import datetime
import re
from core import utils
from core import tts

def handle(mic, comamnd, profile):
    now = datetime.datetime.now()
    hwavlist = utils.find_wav_from_number(now.hour)
    mwavlist = utils.find_wav_from_number(now.minute)
    result = [] 
    if now.minute == 0:
        result = ["bay_gio_la.wav"] + hwavlist + ["gio.wav"]
    else:
        result = ["bay_gio_la.wav"] + hwavlist + ["gio.wav"] + mwavlist + ["phut.wav"]
    tts.speak_wav(*result)

def isMatch(command):
    return command == u"MẤY GIỜ RỒI" or bool(re.search(r"\bMAASY GIOWF\b", command, re.IGNORECASE))
