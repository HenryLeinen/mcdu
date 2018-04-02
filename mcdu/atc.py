from mcdu.subsystem import Subsystem
from mcdu.page import Page, Field

import time

class ATC(Subsystem):
    name = "ATC"

    def __init__(self, api):
        Subsystem.__init__(self)
        self.api = api
        self.midn = 0
        self.status = ""
        self.act = ""
        self.next = ""
        self.callsign = ""

    def run(self):
        i = 0
        while self.running:
            if not i % 10:
                self.fetch_messages()
                print(self.status)

                if self.next:
                    self.logon(self.next)

            time.sleep(1)
            i = i + 1

        self.logoff()

    def fetch_messages(self):
        if not self.callsign: return
        messages = self.api.poll_cpdlc(self.callsign)

        for message in messages:
            self.parse_message(message)

    def parse_message(self, message):
        cpdlc = message[3].split("/")

        dtype, midn, mrn, ra, msg = cpdlc[1:6]

        if dtype != "data2": return
        if not midn or not ra or not msg: return

        print(midn, mrn, ra, msg)

        self.act = message[0]

        if self.status == "sent":
            if msg == "LOGON ACCEPTED":
                self.next = ""
                self.status = "accepted"
            else:
                self.act = ""
                self.status = "rejected"

            return

        if msg == "HANDOVER":
            self.next = msg.split("@")[1]
            return

        if msg == "LOGOFF":
            self.status = ""
            self.act = ""
            self.next = ""
            return

    def logon(self, station):
        self.status = ""
        self.send_message(station, "", "Y", "REQUEST LOGON")
        self.status = "sent"

    def logoff(self):
        if not self.act: return
        self.send_message(self.act, "", "N", "LOGOFF")

    def send_message(self, receiver, mrn, ra, msg):
        msg = "/data2/%i/%s/%s/%s" % (self.midn, mrn, ra, msg)
        self.api.cpdlc(self.callsign, receiver, msg)
        self.midn += 1

    def activate(self):
        self.mcdu.show(LogonPage)

class LogonPage(Page):
    title = "ATC LOGON"

    def init(self):
        self.station = ""
        
        self.field(0, "LOGON TO", 4, format=Field.icao, update=self.logon_to)
        self.field(0, "STATUS", "LOGON>", action=self.logon)
        self.field(1, "FLT NO", 7, format=Field.flightno, update=self.callsign)
        self.field(2, "ATC COMM", "<SELECT OFF", action=self.comm_off)
        self.field(2, "ACT CTR", "")
        self.field(3, "", "")
        self.field(3, "NEXT CTR", "")
        self.field(4, "ADS ARM", "<SELECT OFF", action=self.ads_arm)
        self.field(4, "ADS EMERG", "SELECT ON>", action=self.ads_emerg)

    def logon_to(self, value):
        self.station = value

    def logon(self):
        if self.station:
            self.sys.logon(self.station)
            self.field_update(0, 1, "SENT")

    def callsign(self, value):
        self.sys.callsign = value

    def comm_off(self):
        pass

    def ads_arm(self):
        pass

    def ads_emerg(self):
        pass

    def index(self):
        pass
