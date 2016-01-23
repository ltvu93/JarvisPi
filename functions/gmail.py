# coding: utf-8
import re
import imaplib
import email

from core import tts

USERNAME = 'shiva9u1@gmail.com'
PASSWORD = 'sonyuhshidae93'

def getSender(email):

	sender = email['From']
	match = re.match(r'(.*)\s<.*>', sender)
	if match:
		return match.group(1)

	return sender

def getMostRecentDate(emails):

    dates = [getDate(e) for e in emails]
    dates.sort(reverse=True)
    if dates:
        return dates[0]
    return None

def getUnreadEmails(limit = None):
	"""
	Go to link: https://www.google.com/settings/security/lesssecureapps
	And turn on to access gmail from JarvisPi
	"""
	conn = imaplib.IMAP4_SSL('imap.gmail.com')
	conn.login(USERNAME, PASSWORD)

	# Select inbox or default namespace
	conn.select(readonly=1)
	# Get emails unread
	(retcode, messages) = conn.search(None, '(UNSEEN)')

	if retcode == 'OK':
		numUnread = len(messages[0].split(' '))
		if limit and numUnread > limit:
			return numUnread

		msgs = []
        for num in reversed(messages[0].split(' ')):
        	typ, data = conn.fetch(num,'(RFC822)')
        	msg = email.message_from_string(data[0][1])
        	msgs.append(msg)

	conn.close()
	conn.logout()

	return msgs

def handle(mic, comamnd, profile):

	try:
		msgs = getUnreadEmails(limit = 5)
	except imaplib.IMAP4.error:
		tts.speak_wav("dang_nhap_gmail_that_bai.wav")
		return

	if isinstance(msgs, int):
		respond = "Bạn có %d thư chưa đọc" % msgs
		mic.speak(respond)
		return

	senders = [getSender(msg) for msg in msgs]

	if not senders:
		tts.speak_wav("ban_khong_co_thu_moi.wav")
	elif len(senders) == 1:
		mic.speak("Bạn có 1 thư mới từ %s", senders[0])
	else:
		response = "Bạn có %d thư mới " % len(senders)
		unique_senders = list(set(senders))
		if len(unique_senders) > 1:
			response += " từ "
			response += ", ".join(unique_senders)
		else:
			response += "từ %s" % unique_senders[0]

		mic.speak(response)

def isMatch(command):
	return bool(re.search(ur"\bCẬP NHẬT HỘP THƯ\b", command, re.IGNORECASE)) or bool(re.search(r"\bHOOJP THUW\b", command, re.IGNORECASE))
