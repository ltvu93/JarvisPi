import RPi.GPIO as GPIO
import time

class Signal:
    def __init__(self, num):
        self.light = num
        GPIO.setmode(GPIO.BCM)
        self.isblink = False
        GPIO.setup(self.light, GPIO.OUT)
        GPIO.output(self.light, False) 
        self.p = GPIO.PWM(self.light, 3)

    def turn_on(self):
        GPIO.output(self.light, True)
        
    def turn_off(self):
        GPIO.output(self.light, False)   
    
    def start_blink(self):
        self.isblink = True
        self.p.ChangeFrequency(3)
        self.p.ChangeDutyCycle(50)
        self.p.start(50)
        time.sleep(0.5)

    def stop_blink(self):
        self.isblink = False
        self.p.stop()
        time.sleep(0.5)
        #self.turn_off()

    def clean_up(self):
        GPIO.cleanup()

    def get_status(self):
        return GPIO.input(self.light)

    
