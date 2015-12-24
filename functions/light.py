# coding: utf-8
#import RPIO 		  #https://pythonhosted.org/RPIO/
from core import tts

LIGHT_ONE = 11
LIGHT_TWO = 13

# RPIO.setmode(RPIO.BOARD)
# RPIO.setup(LIGHT_ONE, RPIO.OUT, initial=RPIO.HIGH)
# RPIO.setup(LIGHT_TWO, RPIO.OUT, initial=RPIO.HIGH)

def handle(mic, command):
	if command == u"BẬT ĐÈN":
		# RPIO.output(LIGHT_ONE, RPIO.LOW)
		# RPIO.output(LIGHT_TWO, RPIO.LOW)
		tts.espeak_tts("Đã bật đèn")
	elif command == u"TẮT ĐÈN":
		# RPIO.output(LIGHT_ONE, RPIO.HIGH)
		# RPIO.output(LIGHT_TWO, RPIO.HIGH)
		tts.espeak_tts("Đã tắt đèn")

def isMatch(command):
	return command == u"BẬT ĐÈN" or command == u"TẮT ĐÈN"
	