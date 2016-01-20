# coding: utf-8
import os

import tts
import apppath

from signal import Signal
from brain import Brain
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
                        
			print "Start listening keyword '%s'" % self.nickname
			self.mic.passiveListen(self.nickname)
			print "Stop listening keyword '%s'" % self.nickname

			print "Start listening command"
			commands = self.mic.activeListenToAllOptions()
			print "Stop listening command"
			if commands:
				print commands
				self.brain.process(commands)
			else:
                                self.mic.speak("Không nghe rõ lệnh")
