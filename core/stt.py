# coding: utf-8
import logging

import requests
import urllib
import urlparse
import json
import apppath

import wave

import sphinxbase
import pocketsphinx as ps
from pocketsphinx import *

hmdir = apppath.RESOURCES_PATH + "/model_parameters/jarvispi.cd_cont_200"
lmd   = apppath.RESOURCES_PATH + "/etc/jarvispi.lm.DMP"
dictd = apppath.RESOURCES_PATH + "/etc/jarvispi.dic"
hmdir_bi = apppath.RESOURCES_PATH + "/bi_model/model_parameters/jarvispi.cd_cont_200"
dictd_bi = apppath.RESOURCES_PATH + "/bi_model/etc/jarvispi.dic"

class STT:
	def get_value(self):
		return ""

class GoogleSTT(STT):
	def _regenerate_request_url(self):
		query = urllib.urlencode({'output': 'json',
								'client': 'chromium',
								'lang': 'vi',
								'key': 'AIzaSyDA_NpkLWTkCaVIIho8u8FTjlF-WdJQu_E',
								'maxresults': 6,
								'pfilter': 2})
		return urlparse.urlunparse(('https', 'www.google.com', '/speech-api/v2/recognize', '', query, ''))
		
	def get_value(self, fp):
		wav = wave.open(fp, 'rb')
		frame_rate = wav.getframerate()
		wav.close()
		data = fp.read()

		urls = self._regenerate_request_url()
		headers = {'content-type': 'audio/l16; rate=%s' % frame_rate}
		
		try:
			r = requests.post(urls, data = data, headers = headers)
			r.raise_for_status()
		except requests.exceptions.HTTPError:
			print 'Request failed with http status %d' % r.status_code

			if r.status_code == requests.codes['forbidden']:
				print 'Status 403 is probably caused by an invalid Google API key.'
				return []

		r.encoding = 'utf-8'

		try:
			response = json.loads(list(r.text.strip().split('\n', 1))[-1])

			if len(response['result']) == 0:
			# Response result is empty
				raise ValueError('Nothing has been transcribed.')

			results = [alt['transcript'] for alt in response['result'][0]['alternative']]

		except ValueError as e:
					print 'Empty response: %s' % e.args[0]
					results = []

		except (KeyError, IndexError):
					#self._logger.warning('Cannot parse response.', exc_info=True)
					results = []
		else:
			#Convert all results to lowercase
			results = tuple(result.upper() for result in results)
			return results

class PocketSphinxSTT(STT):
	def __init__(self, mode='passive'):
		self.logger = logging.getLogger(__name__)
		
		config = Decoder.default_config()
		
		if(mode == 'passive'):
                        config.set_string('-hmm', hmdir_bi)
                        config.set_string('-dict', dictd_bi)
			config.set_string('-keyphrase', "bi")
			config.set_float('-kws_threshold', 1e-20)		
		else:
                        config.set_string('-hmm', hmdir)
                        config.set_string('-dict', dictd)
			config.set_string('-lm', lmd)
			config.set_string('-logfn', '/dev/null')

		self.decoder = ps.Decoder(config)
		
	def listen_hot_keyword(self, keyword, stream):
		self.decoder.start_utt()
		stream.start_stream()
		
		while True:
			buf = stream.read(1024)
			self.decoder.process_raw(buf, False, False)
			if self.decoder.hyp() != None and self.decoder.hyp().hypstr == keyword.lower():
				#self.logger.info("Detected keyword: " + keyword)
                                #print "Detected keyword: " + keyword
				self.decoder.end_utt()
				stream.stop_stream()
				stream.close()
				return
		
	def get_value(self, fp):
		result = []
		data = fp.read()
		self.decoder.start_utt()
		self.decoder.process_raw(data, False, False)
		self.decoder.end_utt()
		hyp = self.decoder.hyp()
		try:
			if self.decoder.hyp().hypstr != "":
				result.append(self.decoder.hyp().hypstr.upper())
		except AttributeError:
			print "Can not regconize anything. Please speak again"
			pass
		return result
