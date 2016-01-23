# coding: utf-8
import re
import feedparser 		#https://wiki.python.org/moin/RssLibraries
import time

from core import utils
from core import tts


def getTruePostSummary(summary):
	index = summary.index("</a>")
	return summary[index+4:]

def handle(mic, comamnd, profile):
	if u"TIN TỨC THỜI SỰ" in comamnd:
		url = 'http://vnexpress.net/rss/thoi-su.rss'
		rssTitle = "TIN THỜI SỰ"
	else:
		url = 'http://vnexpress.net/rss/tin-moi-nhat.rss'
		rssTitle = "TIN MỚI NHẤT"
	try:
		data = feedparser.parse(url)	
	except:
		tts.speak_wav("ket_noi_mang_that_bai.wav")
		return
	mic.speak(rssTitle)

	for post in data.entries:
		title = post.title.encode('utf-8')
		summmary = getTruePostSummary(post.summary.encode('utf-8'))
		#link = post.link
                
		mic.speak("Bài viết với tiếu đề ," + title)
		#time.sleep(0.5)
		mic.speak("Nội dung, " + summmary)
		
		
		while True:
			tts.speak_wav("ban_co_muon_tiep_tuc_hay_khong.wav")
			command = mic.activeListen()
			
			mic.get_signal().turn_off()
			mic.get_signal().start_blink()
			if not command:
                                continue
			elif command == u"CÓ" or command == "COS":
                                break
                        elif command == u"KHÔNG" or command == u"KHOONG":
                                tts.speak_wav("ket_thuc_doc_tin_tuc.wav")
                                mic.get_signal().stop_blink()
                                return

		#tts.online_speak("Kết thúc đọc tin tức")

def isMatch(command):
        return bool(re.search(ur"\bTIN TỨC\b", command, re.IGNORECASE)) or bool(re.search(r"\bTIN TUWSC\b", command, re.IGNORECASE))
