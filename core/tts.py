# coding: utf-8
import os
import tempfile
import subprocess
from gtts import gTTS

def espeak_tts(phrase):
	subprocess.call(['espeak', '-v', 'vi+m2', '-s', '100', phrase], shell=True)

def speak(filePath):
	subprocess.call(['start', 'wmplayer', filePath], shell=True)

def gg_tts(phrase):
	tts = gTTS(text=phrase, lang='vi')
	with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
		fpath = f.name
		print fpath
	tts.save(fpath)
	speak(fpath)
	os.remove(fpath)