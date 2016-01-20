# coding: utf-8
import logging
import re
import mpd

class MusicMode():
    def __init__(self, nickname, mic, mpdplayer):
        self._logger = logging.getLogger(__name__)
        self.nickname = nickname
        self.music = mpdplayer
        self.mic = mic

    def delegateInput(self, command):

    	if command == u"MỞ NHẠC" or command == "MOWR NHAJC":
    		self.mic.speak("Playing %s" % self.music.current_song())
    		self.music.play()
    	elif command == u"DỪNG NHẠC" or command == "DUWFNG NHAJC":
    		self.music.stop()
    	elif command == "PAUSE":
    		player.pause(1)
    	elif command == "RESUME":
    		player.pause(0)
    	elif command == "NEXT":
    		self.music.play()
    		player.next()
    	elif command == "PREVIOUS":
    		self.music.play()
    		player.previous()
    	elif command == u"TĂNG ÂM LƯỢNG NHẠC" or command == "TAWNG AAM LUWOWNG NHAJC":
    		player.volume(interval=10)
    		self.music.play()
    	elif command == u"GIẢM ÂM LƯỢNG NHẠC" or command == "GIARM AAM LUWOWNG NHAJC":
    		player.volume(interval=-10)
    		self.music.play()

    def handleForever(self):

        self.music.play()
        #self.mic.say("Đang chơi bài %s" % self.music.current_song())

        while True:

            threshold, transcribed = self.mic.passiveListen(self.nickname)

            if not transcribed or not threshold:
                self._logger.info("Nothing has been said or transcribed.")
                continue

            self.music.pause()

            command = self.mic.activeListen()

            if command:
                if "DỪNG NHẠC" in command:
                    return
                self.delegateInput(command)
            else:
                self.mic.say("Không nghe rõ lệnh?")
                self.music.play()

class Song():
	def __init__(self, title, artist, album):
		self.title = title
		self.artist = artist
		self.album = album

class MPDPlayer():
	def __init__(self):
		self.client = mpd.MPDClient()
		self.client.use_unicode = True
		self.client.timeout = None
		self.client.idletimeout = None

		self.client.connect("localhost", 6600)

		self.songs = []

		currentplaylist = self.client.playlistinfo()
		if not currentplaylist:
			for fileSong in self.client.list('file'):
				self.client.add(fileSong)

		for raw in self.client.playlistinfo():
			title = raw["title"].strip().upper()
			artist = raw["artist"].strip().upper()
			album = raw["album"].strip().upper()

			self.songs.append(Song(title, artist, album))
	
	def reconnect():
		try:
			client.connect("localhost", 6600)
		except:
			pass

	def play(self):
		self.client.play()

	def next(self):
		self.client.next()

	def previous(self):
		self.client.previous()

	def stop(self):
		self.client.stop()

	def volume(self, level):
		self.client.setvol(int(level))

def handle(mic, command, profile):

	mic.speak("Đang lấy dữ liệu nhạc trên máy")
	try:
		mpdplayer = MPDPlayer()
	except:
		mic.say("Không thể lấy dữ liệu nhạc trên máy")
	print "Đang vào chế độ nghe nhạc"
	music_mode = MusicMode("Bi", mic, mpdplayer)
	music_mode.handleForever()
	print "Thoát chế độ nghe nhạc"

def isMatch(command):
	return bool(re.search(ur"\NHẠC|NHACJC\b", command, re.IGNORECASE))
