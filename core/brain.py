# coding: utf-8
import logging
import apppath
import pkgutil
import tts

class Brain():
	def __init__(self, mic, profile):
		self.logger = logging.getLogger(__name__)
		self.profile = profile
		self.mic = mic
		self.signal = mic.get_signal()
		self.functions  = self.getFunctions()

	def getFunctions(self):
		"""Get all functions available of JarvisPi"""

		functions = []
		locations = [apppath.FUNCTIONS_PATH]
		for finder, name, ispkg in pkgutil.walk_packages(locations):
			try:
				# Check functions in JarvisPi
				loader = finder.find_module(name)
				mod = loader.load_module(name)
			except:
				self.logger.warning("Cannot load functions '%s'", name)
			else:
				functions.append(mod)

		return functions

	def process(self, commands):
		"""Process user command"""
                
		for function in self.functions:
			for command in commands:
				match = function.isMatch(command)
				if match:
                                        self.signal.start_blink()
					function.handle(self.mic, command, self.profile)
					self.signal.stop_blink()
					return

		#TODO: speak cannot understant commands
		tts.speak_wav("khong_tim_thay_lenh.wav")
