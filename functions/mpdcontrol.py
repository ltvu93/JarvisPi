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

    	if command == u"BẬT NHẠC" or command == "BAAJT NHAJC":
    		#self.mic.speak("Playing %s" % self.music.current_song())
    		self.music.play()
    		return
    	elif command == u"DỪNG NHẠC" or command == "DUWFNG NHAJC":
    		self.music.stop()
    		return
    	elif command == u"TIẾP THEO":
    		self.music.play()
    		self.music.next()
    		return
    	elif command == u"LÙI LẠI":
    		self.music.play()
    		self.music.previous()
    		return

    	self.music.play()
    	self.mic.speak("Không tìm thấy lệnh")

    def handleForever(self):

        self.music.play()
        #self.mic.say("Đang chơi bài %s" % self.music.current_song())
        while True:

            #Listen keyword to wake up JarvisPi in music mode
            self.mic.passiveListen(self.nickname)

            self.music.pause()
            
            #Listen music mode command
            command = self.mic.activeListen()
            
            self.mic.get_signal().start_blink()

            if command:
                if command == u"TẮT NHẠC":
                    self.mic.get_signal().stop_blink()
                    #TODO: reset lai mpd player.
                    return
                self.delegateInput(command)
            else:
                self.mic.speak("Không nghe rõ lệnh")
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
		self.client.timeout = 10
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
		
	def pause(self):
		self.client.pause()

	def volume(self, level):
		self.client.setvol(int(level))

def handle(mic, command, profile):

	mic.speak("Đang lấy dữ liệu nhạc trên máy")
	try:
		mpdplayer = MPDPlayer()
	except:
		mic.speak("Không thể lấy dữ liệu nhạc trên máy")
	mic.speak("Đang vào chế độ nghe nhạc")
	music_mode = MusicMode("Bi", mic, mpdplayer)
	music_mode.handleForever()
	mic.speak("Thoát chế độ nghe nhạc")

def isMatch(command):
	return bool(re.search(ur"\NHẠC|NHACJC\b", command, re.IGNORECASE))
