# coding: utf-8
import datetime
from core import converter

def handle(mic, comamnd):
    now = datetime.datetime.now()
    response = "Bây giờ là %d giờ %d phút" % (now.hour, now.minute)
    mic.get_tts().speak(converter.find_num_and_replace(response))

def isMatch(command):
    return command == u"MẤY GIỜ RỒI" or command == "THOWFI GIAN"
