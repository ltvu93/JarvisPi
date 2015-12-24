# coding: utf-8
import logging

import requests
import urllib
import urlparse
import json

import wave

def _regenerate_request_url():
	query = urllib.urlencode({'output': 'json',
							'client': 'chromium',
							'lang': 'vi',
							'key': 'AIzaSyARC6Vdp5i_A4d9g_5hiLydjr2jbjCmf2s',
							'maxresults': 6,
							'pfilter': 2})
	
	return urlparse.urlunparse(
		('https', 'www.google.com', '/speech-api/v2/recognize', '',
			query, ''))

def gg_transale(fp):
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