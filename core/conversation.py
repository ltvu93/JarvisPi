# coding: utf-8
import os

import tts
import apppath


from mic import Mic
from brain import Brain
from signal import Signal
from stt import *

class Conversation():
	def __init__(self, nickname, profile):
		self.nickname = nickname
		self.profile = profile
		if profile["stt"]["name"] == "pocketsphinx":
			self.stt = PocketSphinxSTT()
		elif profile["stt"]["name"] == "google":
			self.stt = GoogleSTT()
		self.mic = Mic(self.stt)
		self.signal = Signal(24)
		self.brain = Brain(self.mic, self.signal)
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
