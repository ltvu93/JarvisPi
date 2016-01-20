# coding: utf-8
import os
import urllib2

#APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUNCTIONS_PATH = os.path.join(APP_PATH, 'functions')
RESOURCES_PATH = os.path.join(APP_PATH, 'resources')

def get_config(filename):
	return os.path.join(APP_PATH, filename)

def get_resources(filename):
	return os.path.join(RESOURCES_PATH, filename)

def detect_internet():
        try:
                response=urllib2.urlopen('http://google.com',timeout=1)
                return True
        except urllib2.URLError as err:
                pass
        return False
