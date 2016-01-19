# coding: utf-8
import RPi.GPIO as GPIO 		  #https://pythonhosted.org/GPIO/

LIGHT_ONE = 17
LIGHT_TWO = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_ONE, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(LIGHT_TWO, GPIO.OUT, initial=GPIO.HIGH)

def handle(mic, command):
	if command == u"BẬT ĐÈN" or command == "BAAJT DDEFN":
		GPIO.output(LIGHT_ONE, GPIO.LOW)
		GPIO.output(LIGHT_TWO, GPIO.LOW)
		mic.get_tts().speak("Đã bật đèn")
	elif command == u"TẮT ĐÈN" or command == "TAWST DDEFN":
		GPIO.output(LIGHT_ONE, GPIO.HIGH)
		GPIO.output(LIGHT_TWO, GPIO.HIGH)
		mic.get_tts().speak("Đã tắt đèn")

def isMatch(command):
	return command == u"BẬT ĐÈN" or command == u"TẮT ĐÈN" or command == "BAAJT DDEFN" or command == "TAWST DDEFN"
	
