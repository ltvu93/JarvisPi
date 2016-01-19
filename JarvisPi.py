# coding: utf-8
import logging
import sys
import yaml

from core import apppath
from mic import Mic
from core.conversation import Conversation

class JarvisPi():
	def __init__(self):
		self.logger = logging.getLogger(__name__)

		#Read profile information
		try:
			profile_path = apppath.get_config('profile.yml')
			with open(profile_path, 'r') as f:
				self.profile = yaml.load(f)
		except OSError:
			self.logger.error("Cannot read profile information '%s'.", profile_path)
		
		#New passive_stt
		passive_stt = PocketSphinxSTT()
		
		#New active_stt
		if profile["stt"]["name"] == "pocketsphinx":
			active_stt = PocketSphinxSTT("active")
		elif profile["stt"]["name"] == "google":
			active_stt = GoogleSTT()
		
		self.mic = Mic(passive_stt, active_stt)

	def run(self):
		conversation = Conversation("BI", self.mic, self.profile)
		conversation.handleForever()

if __name__ == "__main__":
	logging.basicConfig()

	try:
		app = JarvisPi()
	except Exception:
		sys.exit(1)

	app.run()