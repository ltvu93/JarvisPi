# coding: utf-8
import logging

import requests
import urllib
import urlparse
import json
import apppath

import wave
from pocketsphinx import *

hmdir = apppath.RESOURCES_PATH + "/model_parameters/jarvispi.cd_cont_200"
lmd   = apppath.RESOURCES_PATH + "/etc/jarvispi.lm.DMP"
dictd = apppath.RESOURCES_PATH + "/etc/jarvispi.dic"

import pocketsphinx as ps
import sphinxbase

config = Decoder.default_config()
config.set_string('-hmm', hmdir)
config.set_string('-lm', lmd)
config.set_string('-dict', dictd)
config.set_string('-logfn', '/dev/null')
print hmdir
decoder = ps.Decoder(config)


def _regenerate_request_url():
	query = urllib.urlencode({'output': 'json',
							'client': 'chromium',
							'lang': 'vi',
							'key': 'AIzaSyDA_NpkLWTkCaVIIho8u8FTjlF-WdJQu_E',
							'maxresults': 6,
							'pfilter': 2})
	
	return urlparse.urlunparse(
		('https', 'www.google.com', '/speech-api/v2/recognize', '',
			query, ''))
	

class STT:
	def get_value(self):
		return ""

class GoogleSTT(STT):
	def get_value(self, fp):
		wav = wave.open(fp, 'rb')
		frame_rate = wav.getframerate()
		wav.close()
		data = fp.read()

		urls = _regenerate_request_url()
		headers = {'content-type': 'audio/l16; rate=%s' % frame_rate}
		r = requests.post(urls, data = data, headers = headers)

		try:
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
	def get_value(self, fp):
	   	# except RuntimeError, e:
	   	#     print e
	   	# 	exit()
                result = []    
                fp.seek(44)
                data = fp.read()
                decoder.start_utt()
                decoder.process_raw(data, False, True)
                decoder.end_utt()
                hyp = decoder.hyp()
                try:
                        if hyp.hypstr != "":
                                result.append(hyp.hypstr.upper())
                except AttributeError:
			print "Can not regconize anything. Please speak again"
			pass
                return result
