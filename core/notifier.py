# coding: utf-8
import logging
import Queue
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from functions import gmail

class Notifier():
    class NotificationClient():
    	def __init__(self, gather, timestamp):
            self.gather = gather
            self.timestamp = timestamp
        def run(self):
            self.timestamp = self.gather(self.timestamp)

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.q = Queue.Queue()
        self.notifiers = []

        self.notifiers.append(self.NotificationClient(
                self.handleEmailNotifications, None))

        sched = BackgroundScheduler(timezone="UTC", daemon=True)
        sched.start()
        sched.add_job(self.gather, 'interval', seconds=30)
        atexit.register(lambda: sched.shutdown(wait=False))
    
    def gather(self):
        for client in self.notifiers:
            client.run()

    def handleEmailNotifications(self, lastDate):
        # emails = gmail.getUnreadEmails(since=lastDate)
        # if emails:
        #     lastDate = gmail.getMostRecentDate(emails)

        # def styleEmail(e):
        #     return "Có email mới từ %s." % gmail.getSender(e)

        # for e in emails:
        #     self.q.put(styleEmail(e))

        return lastDate

    def getNotification(self):
        try:
            notif = self.q.get(block=False)
            return notif
        except Queue.Empty:
            return None

    def getAllNotifications(self):
        notifs = []

        notif = self.getNotification()
        while notif:
            notifs.append(notif)
            notif = self.getNotification()

        return notifs