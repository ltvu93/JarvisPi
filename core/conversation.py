# coding: utf-8
import os

import tts
import apppath

from mic import Mic
from brain import Brain
from notifier import Notifier

class Conversation():
	def __init__(self, nickname, profile):
		self.nickname = nickname
		self.profile = profile
		self.mic = Mic()
		self.brain = Brain(self.mic)
		#self.notifier = Notifier()

	def handleForever(self):
		"""Handle interact bettwen user and JarvisPi."""

		while True:
                        '''
			notifications = self.notifier.getAllNotifications()
			for notif in notifications:
				print str(notif)
                        '''
			print "Start listening keyword '%s'" % self.nickname
			result = self.mic.passiveListen(self.nickname)
			print "Stop listening keyword '%s'" % self.nickname

			if result:
				print "Start listening command"
				#tts.speak(apppath.get_resources('yes.mp3'))
				tts.speak(apppath.get_resources('yes.wav'))
				commands = self.mic.activeListen()
				print "Stop listening command"
				if commands:
					print commands
					self.brain.process(commands)
