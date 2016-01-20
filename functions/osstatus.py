# coding: utf-8
import re
import psutil     #https://pypi.python.org/pypi/psutil
import platform
import datetime
import time

from core import tts

def handle(mic, comamnd, profile):
	os, name, version, _, _, _ = platform.uname()
	version = version.split('-')[0]
	cores = psutil.cpu_count()
	cpu_percent = psutil.cpu_percent()
	memory_percent = psutil.virtual_memory()[2]
	disk_percent = psutil.disk_usage('/')[3]
	'''
	response = "Tôi đang chạy hệ điều hành %s phiên bản %s.  " %(os, version)
	response += "Hệ thống tên %s và có CPU %s nhân.   " %(name, cores)
	response += "CPU hiện tại được sử dụng %s phần trăm.  " %cpu_percent
	response += "Bộ nhớ hiện tại được sử dụng %s phần trăm." %memory_percent
	response += "Ổ cứng hiện tại được sử dụng %s phần trăm." %disk_percent
	'''
	mic.speak("Tôi đang chạy hệ điều hành %s phiên bản %s." %(os, version))
	time.sleep(0.5)
	mic.speak("Hệ thống tên %s và có CPU %s nhân." %(name, cores))
	time.sleep(0.5)
	mic.speak("CPU hiện tại được sử dụng %s phần trăm." %cpu_percent)
	time.sleep(0.5)
	mic.speak("Bộ nhớ hiện tại được sử dụng %s phần trăm." %memory_percent)
	time.sleep(0.5)
	mic.speak("Ổ cứng hiện tại được sử dụng %s phần trăm." %disk_percent)
	mic.speak(response)

def isMatch(command):
    #return command == u"MÀY SAO RỒI"
    return bool(re.search(ur"\bTRẠNG THÁI VẬN HÀNH\b", command, re.IGNORECASE)) or bool(re.search(r"\bTRAJNG THASI VAAJN HAFNH\b", command, re.IGNORECASE))
