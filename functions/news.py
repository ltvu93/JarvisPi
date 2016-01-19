# coding: utf-8
import re
import feedparser 		#https://wiki.python.org/moin/RssLibraries

from core import converter

def getTruePostSummary(summary):
	index = summary.index("</a>")
	return summary[index+4:]

def handle(mic, comamnd):
	try:
		url = 'http://vnexpress.net/rss/tin-moi-nhat.rss'
		data = feedparser.parse(url)	

		rssTitle = data['feed']['title'].encode('utf-8')
	except:
		mic.get_tts().speak("Kết nối mạng có vấn đề.      ")
		mic.get_tts().speak("Vui lòng thử lại.      ")
		return
	mic.get_tts().speak(rssTitle)

	for post in data.entries:
		title = post.title.encode('utf-8')
		summmary = getTruePostSummary(post.summary.encode('utf-8'))
		#link = post.link

		mic.get_tts().speak(converter.find_num_and_replace(title + ". " + summmary))
		
		while True:
			mic.get_tts().speak("Bạn có muốn tiếp tục hay không")
			commands = mic.activeListen()
			if commands:
				if any(command == u"CÓ" for command in commands):
					break
				elif any(command == "COS" for command in commands):
					break
				elif any(command == u"KHÔNG" for command in commands):
                                        mic.get_tts().speak("Kết thúc đọc tin tức")
					return
				elif any(command == u"KHOONG" for command in commands):
                                        mic.get_tts().speak("Kết thúc đọc tin tức")
					return

		#tts.online_speak("Kết thúc đọc tin tức")

def isMatch(command):
        return bool(re.search(ur"\bTIN TỨC\b", command, re.IGNORECASE)) or bool(re.search(ur"\bTIN TỨC\b", command, re.IGNORECASE))
