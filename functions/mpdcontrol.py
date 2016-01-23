# coding: utf-8
import logging
import re
import mpd

from core import tts

class MusicMode():
    def __init__(self, nickname, mic, mpdplayer):
        self._logger = logging.getLogger(__name__)
        self.nickname = nickname
        self.music = mpdplayer
        self.mic = mic

    def delegateInput(self, command):

        print command

    	if command == u"BẬT NHẠC" or command == "BAAJT NHAJC":
    		#self.mic.speak("Playing %s" % self.music.current_song())
    		self.music.play()
    		return
    	elif command == u"PHÁT TẤT CẢ" or command == "PHAST TAAST CAR":
            self.music.load_all_songs()
            self.music.play()
            return
        elif u"PHÁT NHẠC CỦA " in command or "PHAST NHAJC CUAR " in command:
            artist = command.replace(u"PHÁT NHẠC CỦA ","").replace("PHAST NHAJC CUAR ","")
            if artist:
                result = self.music.load_songs_of_artist(artist)
                if result:
                    #self.mic.speak("Đang chơi nhạc của " + artist.encode("utf-8"))
                    print ""
                else:
                    #self.mic.speak("Không tìm thấy nhạc của " + artist.encode("utf-8"))
                    tts.speak_wav("khong_tim_thay_nhac_yeu_cau.wav")
                    print ""
                self.music.play()
            else:
                tts.speak_wav("khong_tim_thay_lenh.wav")
            return

    	elif command == u"DỪNG NHẠC" or command == "DUWFNG NHAJC":
    		self.music.stop()
    		return
    	
    	elif command == u"TIẾP THEO" or command == "TIEESP THEO":
    		self.music.play()
    		self.music.next()
    		return
    	elif command == u"LÙI LẠI" or command == "LUFI LAJI" or command == "QUAY LẠI":
    		self.music.play()
    		self.music.previous()
    		return

    	self.music.play()
    	tts.speak_wav("khong_tim_thay_lenh.wav")

    def handleForever(self):

        self.music.play()
		
        while True:

            #Listen keyword to wake up JarvisPi in music mode
            self.mic.passiveListen(self.nickname)

            self.music.pause()
            
            #Listen music mode command
            command = self.mic.activeListen()
            
            self.mic.get_signal().start_blink()

            if command:
                if command == u"TẮT NHẠC" or command == "TAWST NHAJC":
                    self.mic.get_signal().stop_blink()
                    self.music.disconnect()
                    return
                self.delegateInput(command)
            else:
                tts.speak_wav("khong_nghe_ro_lenh.wav")
                self.music.play()

class Song():
	def __init__(self, id, file, title, artist, album):
		self.id = id
		self.file = file
		self.title = title
		self.artist = artist
		self.album = album
	def getId(self):
		return self.id
	    
	def showInfo(self):
                print self.id
                print self.file
		print self.title
		print self.artist

class MPDPlayer():
	def __init__(self):
		self.client = mpd.MPDClient()
		self.client.use_unicode = True
		self.client.timeout = 10
		self.client.idletimeout = None

		self.client.connect("localhost", 6600)

                self.songs = []
		self.current_songs = []
		
		self.load_all_songs()
	
	def reconnect(self):
		try:
			client.connect("localhost", 6600)
		except:
			pass

	def disconnect(self):
		self.client.clear()
		self.client.close()
		self.client.disconnect()
			
	def current_song(self):
		try:
			raw_song = self.client.playlistinfo(int(self.client.status()["song"]))[0]
			id = int(raw_song["pos"].strip())
			#file = raw_song["file"].strip().upper()
			#title = raw_song["title"].strip().upper()
			#artist = raw_song["artist"].strip().upper()
			#album = raw_song["album"].strip().upper()

			#return Song(id, file, title, artist, album)
			return id
		except:
			return None
			
	def load_all_songs(self):
		self.client.clear()

		for fileSong in self.client.list('file'):
			self.client.add(fileSong)
			
		for raw in self.client.playlistinfo():
			id = int(raw["pos"].strip())
			file = raw["file"]
			title = raw["title"].strip().upper()
			artist = raw["artist"].strip().upper()
			album = raw["album"].strip().upper()
			
			self.songs.append(Song(id, file, title, artist, album))
			self.current_songs.append(Song(id, file, title, artist, album))
			
	def load_songs_of_artist(self, artist):
                print artist
                for song in self.songs:
                    print song.showInfo()
		artist_songs = [song for song in self.songs if artist in song.artist]
		
		if artist_songs:
			self.client.clear()
			self.current_songs = []
			for song in artist_songs:
				self.client.add(song.file)
				self.current_songs.append(song)
			return True
		else:
			return False
	
	def play(self, id = None):
		if id == None:
			self.client.play()
		else:
			self.client.play(id)

	def next(self):
		cur_pos = self.current_song()
		if cur_pos == len(self.current_songs) - 1:
                        self.play(0)
		else:
			self.client.next()

	def previous(self):
		cur_pos = self.current_song()
		if cur_pos == 0:
			self.play(len(self.current_songs) - 1)
		else:
			self.client.previous()

	def stop(self):
		self.client.stop()
		
	def pause(self):
		self.client.pause()

	def volume(self, level):
		self.client.setvol(int(level))

def handle(mic, command, profile):

	#tts.speak_wav("bat_dau_tim_nhac.wav")
	try:
	    mpdplayer = MPDPlayer()
	except Exception, e:
            print str(e)
	    tts.speak_wav("khong_tim_thay_nhac.wav")
	    return
	tts.speak_wav("bat_che_do_nghe_nhac.wav")
	music_mode = MusicMode("Bi", mic, mpdplayer)
	music_mode.handleForever()
	tts.speak_wav("thoat_che_do_nghe_nhac.wav")

def isMatch(command):
	return bool(re.search(ur"\bBẬT NHẠC\b", command, re.IGNORECASE)) or command == "BAAJT NHAJC"
