# coding: utf-8
import re
import feedparser 		#https://wiki.python.org/moin/RssLibraries
from core import tts

def getTruePostSummary(summary):
	index = summary.index("</a>")
	return summary[index+4:]

def handle(mic, comamnd):
	url = 'http://vnexpress.net/rss/tin-moi-nhat.rss'
	data = feedparser.parse(url)

	rssTitle = data['feed']['title'].encode('utf-8')
	tts.espeak_tts(rssTitle)

	for post in data.entries:
		title = post.title.encode('utf-8')
		summmary = getTruePostSummary(post.summary.encode('utf-8'))
		#link = post.link

		tts.espeak_tts(title)
		tts.espeak_tts(summmary)
		while True:
			tts.espeak_tts("Bạn có muốn tiếp tục hay không")
			commands = mic.activeListen()
			if commands:
				if any(command == u"CÓ" or command == "COS" for command in commands):
					break
				elif any(command == u"KHÔNG" or command == "KHOONG" for command in commands):
					return

		tts.espeak_tts("Kết thúc đọc tin tức")

def isMatch(command):
    return bool(re.search(ur"\bTIN TỨC\b", command, re.IGNORECASE)) or bool(re.search(r"\bTIN TUWSC\b", command, re.IGNORECASE))