# coding: utf-8
import httplib2
import datetime
import argparse
import re

from datetime import datetime
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow
from oauth2client.tools import *
from oauth2client import tools

client_id = '498869212568-9c77o8gpprokbfoeddi3mkjdg9bmbijg.apps.googleusercontent.com'
client_secret = '_s81jR7w9RxZqx3QdbXyiATZ'

# The scope URL for read/write access to a user's calendar data
scope = 'https://www.googleapis.com/auth/calendar'

# Create a flow object. This object holds the client_id, client_secret, and
# scope. It assists with OAuth 2.0 steps to get user authorization and
# credentials.
flow = OAuth2WebServerFlow(client_id, client_secret, scope)

# Create a Storage object. This object holds the credentials that your
# application needs to authorize access to the user's data. The name of the
# credentials file is provided. If the file does not exist, it is
# created. This object can only hold credentials for a single user, so
# as-written, this script can only handle a single user.
storage = Storage('credentials.dat')

# The get() function returns the credentials for the Storage object. If no
# credentials were found, None is returned.
credentials = storage.get()

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

# If no credentials are found or the credentials are invalid due to
# expiration, new credentials need to be obtained from the authorization
# server. The oauth2client.tools.run() function attempts to open an
# authorization server page in your default web browser. The server
# asks the user to grant your application access to the user's data.
# If the user grants access, the run() function returns new credentials.
# The new credentials are also stored in the supplied Storage object,
# which updates the credentials.dat file.
if not credentials or credentials.invalid:
	credentials = run_flow(flow, storage, flags)

# Create an httplib2.Http object to handle our HTTP requests, and authorize it
# using the credentials.authorize() function.
http = credentials.authorize(httplib2.Http())

# The apiclient.discovery.build() function returns an instance of an API service
# object can be used to make API calls. The object is constructed with
# methods specific to the calendar API. The arguments provided are:
#   name of the API ('calendar')
#   version of the API you are using ('v3')
#   authorized httplib2.Http() object that can be used for API calls
service = build('calendar', 'v3', http=http)

def getEventsInDay(profile, mic, date):
	todayStartTime = str(date.strftime("%Y-%m-%d")) + "T00:00:00Z"
	todayEndTime = str(date.strftime("%Y-%m-%d")) + "T23:59:59Z"
	page_token = None
	while True:

		# Gets events from primary calender from each page in present day boundaries
		events = service.events().list(calendarId='primary', pageToken=page_token, timeMin=todayStartTime, timeMax=todayEndTime).execute() 
		
		if(len(events['items']) == 0):
			mic.speak("Bạn không có lịch hôm nay")
			return

		for event in events['items']:

			try:
				eventTitle = event['summary'].encode('utf-8')
				eventRawStartTime = event['start']['dateTime'].split("T")[1]
				startHour, startMinute, temp = eventRawStartTime.split(":", 2)

				#TODO: change time to text to tts
				startMinute = str(startMinute)
				startHour = str(startHour)
				if int(startMinute) == 0:
					mic.speak(eventTitle + " lúc " + startHour + " giờ.")
				else:
					mic.speak(eventTitle + " lúc " + startHour + " giờ " + startMinute + " phút.")

			except KeyError, e:
				print "Failed to convert value of event"
			
		page_token = events.get('nextPageToken')

		if not page_token:
			return

def handle(mic, comamnd, profile):

	date = datetime.now()

	if bool(re.search(u'HÔM NAY|HOOM NAY', comamnd, re.IGNORECASE)):
		getEventsInDay(profile,mic, date)
	elif bool(re.search(u'NGÀY MAI|NGAFY MAI', comamnd, re.IGNORECASE)):
		one_day = datetime.timedelta(days=1)
		date = date + one_day
		getEventsInDay(profile, mic, date)


def isMatch(command):
    return bool(re.search(ur'\bLỊCH TRÌNH|LIJCH TRIFNH\b', command, re.IGNORECASE))
