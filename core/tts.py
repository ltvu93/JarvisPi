# coding: utf-8
import os
import tempfile
import subprocess
from gtts import gTTS

def espeak_tts(phrase):
	#subprocess.call(['espeak', '-v', 'vi+m2', '-s', '100', phrase], shell=True)
        #subprocess.call(['espeak', '-v', 'vi+m2', '-s', '100', phrase])
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            fname = f.name
        cmd = ['espeak', '-v', 'vi+m2',
                         '-s', '85',
                         '-w', fname,
                         phrase]
        cmd = [str(x) for x in cmd]
        subprocess.call(cmd)
        
        speak(fname)
        os.remove(fname)
def speak(filePath):
	#subprocess.call(['start', 'wmplayer', filePath], shell=True)
        subprocess.call(['aplay', filePath])

def gg_tts(phrase):
	tts = gTTS(text=phrase, lang='vi')
	with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
		fpath = f.name
		print fpath
	tts.save(fpath)
	speak(fpath)
	os.remove(fpath)
