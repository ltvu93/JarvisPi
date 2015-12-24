# coding: utf-8
import re

import urllib
import urlparse
import requests
import json

from core import tts

def _generate_weather_url():
	"""
	Go to link: http://openweathermap.org/current

	Example:
	http://api.openweathermap.org/data/2.5/weather?q=ThuDauMot,VN&lang=vi
	&mode=json&units=metric&appid=73537d5230154c507e6e212c03609cd8
	"""
	query = urllib.urlencode({'q': 'ThuDauMot,VN',
							'appid': '73537d5230154c507e6e212c03609cd8',
							'mode': 'json',
							'units': 'metric',
							'lang': 'vi'})
	
	return urlparse.urlunparse(
		('http', 'api.openweathermap.org', '/data/2.5/weather', '',
			query, ''))

def handle(mic, comamnd):
	url = _generate_weather_url()
	rp = requests.get(url)

	try:
		rp.raise_for_status()
	except requests.exceptions.HTTPError:
		print 'Request failed with http status %d' % r.status_code
		return

	try:
		rpJson = json.loads(rp.content)
		if len(rpJson) == 0:
			raise ValueError('Nothing has been transcribed.')
	except ValueError as e:
		print 'Empty response: %s' % e.args[0]
		return
	else:
		weather_desc = rpJson['weather'][0]['description'].encode("utf-8")
		temp = rpJson['main']['temp']
		humidity = rpJson['main']['humidity']

		response = "Hôm nay %s, " % weather_desc
		response += "nhiệt độ trung bình %d độ C, " % temp
		response += "độ ẩm %d phần trăm" % humidity
		tts.espeak_tts(response)


def isMatch(command):
    return bool(re.search(ur"\bTHỜI TIẾT\b", command, re.IGNORECASE))