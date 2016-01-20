# coding: utf-8
import re
import feedparser 		#https://wiki.python.org/moin/RssLibraries

from core import converter

def getTruePostSummary(summary):
	index = summary.index("</a>")
	return summary[index+4:]

def handle(mic, comamnd, profile):
	try:
		url = 'http://vnexpress.net/rss/tin-moi-nhat.rss'
		data = feedparser.parse(url)	

		rssTitle = data['feed']['title'].encode('utf-8')
	except:
		mic.speak("Kết nối mạng có vấn đề.      ")
		mic.speak("Vui lòng thử lại.      ")
		return
	print rssTitle
	mic.speak(rssTitle)

	for post in data.entries:
		title = post.title.encode('utf-8')
		summmary = getTruePostSummary(post.summary.encode('utf-8'))
		#link = post.link

		mic.speak(title + "      " + summmary)
		
		while True:
			mic.speak("Bạn có muốn tiếp tục hay không")
			command = mic.activeListen()
			
			mic.get_signal().turn_off()
			mic.get_signal().start_blink()
			if not command:
                                continue
			elif command == u"CÓ" or command == "COS":
                                break
                        elif command == u"KHÔNG" or command == u"KHOONG":
                                mic.speak("Kết thúc đọc tin tức")
                                mic.get_signal().stop_blink()
                                return

		#tts.online_speak("Kết thúc đọc tin tức")

def isMatch(command):
        return bool(re.search(ur"\bTIN TỨC\b", command, re.IGNORECASE)) or bool(re.search(r"\bTIN TUWSC\b", command, re.IGNORECASE))
