# -*- coding: utf-8 -*-
import requests
from lxml import html
from lxml import etree
import tempfile
import subprocess

def stringify_children(node):
    from lxml.etree import tostring
    from itertools import chain
    parts = ([node.text] +
            list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))

def speak(pharse):
	r = requests.post("http://speechlab.uit.edu.vn/api/index.php", data = {"text": text, "voice":"quoc800"})
	root =  html.fromstring(r.text)
	pre = root.findall(".//pre")
	str_pre =  stringify_children(pre[0]).strip()
	cmd = "mpg123 " + str_pre
	subprocess.call(cmd)
	