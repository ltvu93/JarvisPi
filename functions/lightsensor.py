# coding: utf-8
import RPi.GPIO as GPIO
import light
from core import tts

LIGHT_SENSOR = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_SENSOR, GPIO.IN)

def handle(mic, command):
	isLight = not GPIO.input(LIGHT_SENSOR)
	#isLight = True
	if isLight:
		tts.espeak_tts("Phòng sáng")
		while True:
			tts.espeak_tts("Bạn có muốn tắt đèn không")
			commands = mic.activeListen()
			if commands:
				if any(command == u"CÓ" or command == "COS" for command in commands):
					light.handle(mic, u"TẮT ĐÈN")
					break
				elif any(command == u"KHÔNG" or command == "KHOONG" for command in commands):
					break
	else:
		tts.espeak_tts("Phòng tối")
		while True:
			tts.espeak_tts("Bạn có muốn bật đèn không")
			commands = mic.activeListen()
			if commands:
				if any(command == u"CÓ" or command == "COS" for command in commands):
					light.handle(mic, u"BẬT ĐÈN")
					break
				elif any(command == u"KHÔNG" or command == "KHOONG" for command in commands):
					break


def isMatch(command):
	return command == u"TRẠNG THÁI ÁNH SÁNG" or command == "TRAJNG THASI ASNH SASNG"
