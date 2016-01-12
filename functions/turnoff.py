# coding: utf-8
import sys
from core import tts
import time

def handle(mic, comamnd):
    tts.espeak_tts("BI SẼ TỰ TẮT TRONG 5 GIÂY NỮA")
    x = 5;
    while x >= 1:
        tts.espeak_tts(str(x))
	x -= 1
    tts.espeak_tts("ĐÃ TẮT. HẸN GẶP LẠI BẠN LẦN SAU")
    sys.exit(0)
def isMatch(command):
    return command == u"TẮT ĐI"
