# coding: utf-8
import RPi.GPIO as GPIO 		  #https://pythonhosted.org/GPIO/
from core import tts

LIGHT_ONE = 17
#LIGHT_TWO = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_ONE, GPIO.OUT, initial=GPIO.HIGH)
#GPIO.setup(LIGHT_TWO, GPIO.OUT, initial=GPIO.HIGH)

def handle(mic, command, profile):
	if command == u"BẬT ĐÈN" or command == "BAAJT DDEFN":
		GPIO.output(LIGHT_ONE, GPIO.LOW)
		#GPIO.output(LIGHT_TWO, GPIO.LOW)
		tts.speak_wav("da_bat_den.wav")
	elif command == u"TẮT ĐÈN" or command == "TAWST DDEFN":
		GPIO.output(LIGHT_ONE, GPIO.HIGH)
		#GPIO.output(LIGHT_TWO, GPIO.HIGH)
		tts.speak_wav("da_tat_den.wav")

def isMatch(command):
	return command == u"BẬT ĐÈN" or command == u"TẮT ĐÈN" or command == "BAAJT DDEFN" or command == "TAWST DDEFN"
	
