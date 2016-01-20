import RPi.GPIO as GPIO
import time

class Signal:
    def __init__(self, num):
        self.light = num
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.light, GPIO.OUT)
        self.p = GPIO.PWM(self.light, 3)

    def turn_on(self):
        GPIO.output(self.light, True)
        
    def turn_off(self):
        GPIO.output(self.light, False)   
    
    def start_blink(self):
        self.p.start(50)

    def stop_blink(self):
        self.p.stop()

    def clean_up(self):
        GPIO.cleanup()

    
