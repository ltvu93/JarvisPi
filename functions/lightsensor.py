# coding: utf-8
#import RPIO  			#https://pythonhosted.org/RPIO/
import light
from core import tts

LIGHT_SENSOR = 15

# RPIO.setmode(RPIO.BOARD)
# RPIO.setup(LIGHT_SENSOR, RPIO.IN)

def handle(mic, command):
	#isLight = RPIO.input(LIGHT_SENSOR)
	isLight = True
	if isLight:
		tts.espeak_tts("Phòng sáng")
		while True:
			tts.espeak_tts("Bạn có muốn tắt đèn không")
			commands = mic.activeListen()
			if commands:
				if any(command == u"CÓ" for command in commands):
					light.handle(mic, u"TẮT ĐÈN")
					break
				elif any(command == u"KHÔNG" for command in commands):
					break
	else:
		tts.espeak_tts("Phòng tối")
		while True:
			tts.espeak_tts("Bạn có muốn bật đèn không")
			commands = mic.activeListen()
			if commands:
				if any(command == u"CÓ" for command in commands):
					light.handle(mic, u"BẬT ĐÈN")
					break
				elif any(command == u"KHÔNG" for command in commands):
					break


def isMatch(command):
	return command == u"TRẠNG THÁI ÁNH SÁNG"