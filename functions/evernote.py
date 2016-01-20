# coding: utf-8
from core import tts

from evernote.api.client import EvernoteClient

def handle(mic, comamnd, profile):
	"""
	Go to link: https://dev.evernote.com/doc/start/python.php
	for guide
	"""

	auth_token = profile['evernote']['token']
	client = EvernoteClient(token=auth_token)
	note_store = client.get_note_store()
	
	note = Types.Note()
	note.title = "Ghi chú trên JarvisPi"
	mic.speak("Nội dung ghi chú là gì?")
	content = mic.activeListen()
	note.content = '<?xml version="1.0" encoding="UTF-8"?>'
	note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
	note.content += '<en-note>Note:<br/>'
	note.content += ('%s' % content)
	note.content += '</en-note>'
    
	created_note = note_store.createNote(note)
	mic.speak("Ghi chú thành công")

    #TODO: Add funtions read notes

def isMatch(command):
	return command == u"GHI CHÚ"
