# coding: utf-8
import RPi.GPIO as GPIO 		  #https://pythonhosted.org/GPIO/

from core import tts

FAN = 27


GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN, GPIO.OUT, initial=GPIO.HIGH)

def handle(mic, command, profile):
	if command == u"BẬT QUẠT" or command == "BAAJT QUAJT":
		GPIO.output(FAN, GPIO.LOW)
		#GPIO.output(LIGHT_TWO, GPIO.LOW)
		tts.speak_wav("da_bat_quat.wav")
	elif command == u"TẮT QUẠT" or command == "TAWST QUAJT":
		GPIO.output(FAN, GPIO.HIGH)
		#GPIO.output(LIGHT_TWO, GPIO.HIGH)
		tts.speak_wav("da_tat_quat.wav")

def isMatch(command):
	return command == u"BẬT QUẠT" or command == u"TẮT QUẠT" or command == "BAAJT QUAJT" or command == "TAWST QUAJT"
	
