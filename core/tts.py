# coding: utf-8
import os
import tempfile
import apppath
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

def speak_wav(*fileNames):
    cmd = ['aplay']
    print fileNames
    for name in fileNames:
        cmd.append(apppath.get_resources(name))
    subprocess.call(cmd)
def speak_mp3(filePath):
    subprocess.call(['omxplayer', filePath])

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
                
                
