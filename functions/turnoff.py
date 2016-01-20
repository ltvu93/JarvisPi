# coding: utf-8
import sys
import time

def handle(mic, comamnd, profile):
    mic.speak("BI SẼ TỰ TẮT TRONG 5 GIÂY NỮA")
    x = 5;
    while x >= 1:
        mic.speak(str(x))
	x -= 1
    mic.speak("ĐÃ TẮT. HẸN GẶP LẠI BẠN LẦN SAU")
    sys.exit(0)
def isMatch(command):
    return command == u"TẮT ĐI"
