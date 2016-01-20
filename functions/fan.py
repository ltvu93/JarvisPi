# coding: utf-8
import RPi.GPIO as GPIO 		  #https://pythonhosted.org/GPIO/

FAN = 17
#LIGHT_TWO = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_ONE, GPIO.OUT, initial=GPIO.HIGH)

def handle(mic, command, profile):
	if command == u"BẬT QUẠT" or command == "BAAJT DDEFN":
		GPIO.output(LIGHT_ONE, GPIO.LOW)
		#GPIO.output(LIGHT_TWO, GPIO.LOW)
		mic.speak("Đã bật quạt")
	elif command == u"TẮT QUẠT" or command == "TAWST DDEFN":
		GPIO.output(LIGHT_ONE, GPIO.HIGH)
		#GPIO.output(LIGHT_TWO, GPIO.HIGH)
		mic.speak("Đã tắt quạt")

def isMatch(command):
	return command == u"BẬT QUẠT" or command == u"TẮT QUẠT" or command == "BAAJT QUAJT" or command == "TAWST QUAJT"
	
