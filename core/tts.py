# coding: utf-8
import os
import tempfile
import subprocess
from gtts import gTTS
import requests
from lxml import html
from lxml import etree

def stringify_children(node):
    from lxml.etree import tostring
    from itertools import chain
    parts = ([node.text] +
            list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))

def speak(filePath):
    subprocess.call(['aplay', filePath])

def gg_tts(phrase):
	tts = gTTS(text=phrase, lang='vi')
	with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
		fpath = f.name
		print fpath
	tts.save(fpath)
	speak(fpath)
	os.remove(fpath)

class EspeakTTS:
        def speak(self, pharse):
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:fname = f.name
                cmd = ['espeak', '-v', 'vi+m2',
                                 '-s', '85',
                                 '-w', fname,
                                 phrase]
                cmd = [str(x) for x in cmd]
                subprocess.call(cmd)
                
                speak(fname)
                os.remove(fname)
        def speak_long_sentence(self, filePath):
                subprocess.call(['aplay', filePath])
                
class OnlineTTS:
    def speak(self, pharse):
        r = requests.post("http://speechlab.uit.edu.vn/api/index.php", data = {"text": pharse, "voice":"quoc800"})
        root =  html.fromstring(r.text)
        pre = root.findall(".//pre")
        str_pre =  stringify_children(pre[0]).strip()
        cmd = "mpg123 -f 393360 " + str_pre
        subprocess.call(cmd, shell=True)
    def speak_wav(self, filePath):
        subprocess.call(['aplay', filePath])
    def speak_mp3(self, filePath):
        subprocess.call(['omxplayer', filePath])
                
                
