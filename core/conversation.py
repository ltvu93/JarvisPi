# coding: utf-8
import os

import tts
import apppath

from brain import Brain
from signal import Signal
from stt import *

class Conversation():
	def __init__(self, nickname, mic, profile):
		self.nickname = nickname
		self.profile = profile
		self.mic = mic
		self.brain = Brain(self.mic, self.profile)
		#self.notifier = Notifier()

	def handleForever(self):
		"""Handle interact bettwen user and JarvisPi."""

		while True:
                        '''
			notifications = self.notifier.getAllNotifications()
			for notif in notifications:
				print str(notif)
                        '''
                        self.signal.turn_off()
			print "Start listening keyword '%s'" % self.nickname
			result = self.mic.passiveListen(self.nickname)
			print "Stop listening keyword '%s'" % self.nickname

			if result:
                                self.signal.turn_on()
				print "Start listening command"
				#tts.speak(apppath.get_resources('yes.mp3'))
				tts.speak(apppath.get_resources('yes.wav'))
				commands = self.mic.activeListen()
				print "Stop listening command"
				if commands:
					print commands
					self.brain.process(commands)
