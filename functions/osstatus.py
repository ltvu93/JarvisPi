# coding: utf-8
import re
import psutil     #https://pypi.python.org/pypi/psutil
import platform
import datetime

from core import tts

def handle(mic, comamnd):
	os, name, version, _, _, _ = platform.uname()
	version = version.split('-')[0]
	cores = psutil.cpu_count()
	cpu_percent = psutil.cpu_percent()
	memory_percent = psutil.virtual_memory()[2]
	disk_percent = psutil.disk_usage('/')[3]
	
	response = "Tôi đang chạy hệ điều hành %s phiên bản %s.  " %(os, version)
	response += "Hệ thống tên %s và có CPU %s nhân.   " %(name, cores)
	response += "CPU hiện tại được sử dụng %s phần trăm.  " %cpu_percent
	response += "Bộ nhớ hiện tại được sử dụng %s phần trăm." %memory_percent
	response += "Ổ cứng hiện tại được sử dụng %s phần trăm." %disk_percent
	'''
	tts.espeak_tts("Tôi đang chạy hệ điều hành %s phiên bản %s.  " %(os, version))
	tts.espeak_tts("Hệ thống tên %s và có CPU %s nhân.   " %(name, cores))
	tts.espeak_tts("CPU hiện tại được sử dụng %s phần trăm.  " %cpu_percent)
	tts.espeak_tts("Bộ nhớ hiện tại được sử dụng %s phần trăm." %memory_percent)
	tts.espeak_tts("Ổ cứng hiện tại được sử dụng %s phần trăm." %disk_percent)
	'''
	tts.espeak_tts(response)

def isMatch(command):
    #return command == u"MÀY SAO RỒI"
    return bool(re.search(ur"\bTRẠNG THÁI VẬN HÀNH\b", command, re.IGNORECASE))
