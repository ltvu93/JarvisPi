# coding: utf-8
import RPi.GPIO as GPIO
import light
from core import tts
#from core import off_tts
#from core import text2num

LIGHT_SENSOR = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_SENSOR, GPIO.IN)

def handle(mic, command):
	isLight = not GPIO.input(LIGHT_SENSOR)
	#isLight = True
	if isLight:
		mic.get_tts().speak("Phòng sáng")
		while True:
			mic.get_tts().speak("Bạn có muốn tắt đèn không")
			commands = mic.activeListen()
			if commands:
				if any(command == u"CÓ" for command in commands):
					light.handle(mic, u"TẮT ĐÈN")
					break
				elif any(command == "COS" for command in commands):
                                        light.handle(mic, u"TẮT ĐÈN")
					break
				elif any(command == u"KHÔNG" for command in commands):
					break
				elif any(command == "KHOONG" for command in commands):
					break
	else:
		mic.get_tts().speak("Phòng tối")
		while True:
			mic.get_tts().speak("Bạn có muốn bật đèn không")
			commands = mic.activeListen()
			if commands:
				if any(command == u"CÓ" for command in commands):
					light.handle(mic, u"BẬT ĐÈN")
					break
				elif any(command == "COS" for command in commands):
					light.handle(mic, u"BẬT ĐÈN")
					break
				elif any(command == u"KHÔNG" for command in commands):
					break
				elif any(command == u"KHOONG" for command in commands):
					break


def isMatch(command):
	return command == u"TRẠNG THÁI ÁNH SÁNG" or command == "TRAJNG THASI ASNH SASNG"
