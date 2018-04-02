from mcdu.subsystem import Subsystem
from mcdu.avionics import Avionics
from mcdu.page import Page, Field

import textwrap, time, os

class ACARS(Subsystem):
    name = "ACARS"

    preflight = 1
    inflight = 2
    postflight = 3

    def __init__(self, api):
        Subsystem.__init__(self)
        self.api = api
        self.avionics = Avionics()
        self.state = ACARS.preflight

        self.armed = False
        self.flightno = ""
        self.origin = ""
        self.dest = ""
        self.plan_dep = ""
        self.eta = ""
        self.altrnt = ""
        self.company = ""
        self.progress = []
        self.messages = []

    def run(self):
        i = 0
        while self.running:
            if not i % 10:
                if self.armed: self.progress_update()
                self.fetch_messages()

            time.sleep(1)
            i = i + 1

    def progress_update(self):
        if self.avionics.progress <= len(self.progress):
            return

        for _ in range(self.avionics.progress - len(self.progress)):
            ptime = time.strftime("%H%MZ", time.gmtime())
            self.progress.append(ptime)
            self.report()

        self.refresh()

    def fetch_messages(self):
        if not self.flightno: return

        messages = self.api.poll_acars(self.flightno)
        if len(messages) < 0: return

        messages.extend(self.messages)
        self.messages = messages
        self.refresh()

    def print_message(self, message):
        printer = os.popen("lpr -o media=A6 -o wrap=true", "w")
        data = (message[0], message[1], message[2])
        printer.write("%s %s %s\n\n" % data)
        printer.write(message[3])
        printer.close()

    def activate(self):
        if self.state == ACARS.preflight:
            self.mcdu.show(PreflightPage)
        elif self.state == ACARS.inflight:
            self.mcdu.show(InflightPage)
        elif self.state == ACARS.postflight:
            self.mcdu.show(PostflightPage)

    def report(self):
        message = ["%s/%s" % (self.origin, self.dest)]

        if len(self.progress) > 0:
            message.append("OUT/" + self.progress[0])

        if len(self.progress) > 1:
            message.append("OFF/" + self.progress[1])

        if len(self.progress) > 2:
            message.append("ON/" + self.progress[2])

        if len(self.progress) > 3:
            message.append("IN/" + self.progress[3])

        if len(self.progress) < 3 and self.eta:
            message.append("ETA/" + self.eta)

        self.api.progress(self.flightno, self.company, " ".join(message))

    def inforeq(self, req, apt):
        self.api.inforeq(self.flightno, req, apt)

class IndexPage(Page):
    title = "ACARS MENU"

    def init(self):
        self.field(0, "", "<INITIALIZATION", action=self.initialize)
        self.field(1, "", "<OOOI TIMES", action=self.oooi)
        self.field(2, "", "<RECEIVED MESSAGES", action=self.received_msgs)
        self.field(3, "", "<ATIS", action=self.atis)
        self.field(4, "", "<LINK TEST", action=self.test)
        self.field(4, "", "FREE TEXT>", action=self.text)

    def initialize(self):
        pass

    def oooi(self):
        self.mcdu.show(OOOIPage)

    def received_msgs(self):
        self.mcdu.show(MessagesPage)

    def atis(self):
        pass

    def test(self):
        pass

    def text(self):
        pass

class OOOIPage(Page):
    title = "OOOI TIMES"

    def refresh(self):
        self.clear()

        self.field(0, "OUT", self.format_time(0))
        self.field(1, "OFF", self.format_time(1))
        self.field(2, "ON", self.format_time(2))
        self.field(3, "IN", self.format_time(3))
        self.field(5, "", "<RETURN", action=self.ret)

        Page.refresh(self)

    def format_time(self, index):
        if len(self.sys.progress) > index:
            return self.sys.progress[index]
        else:
            return "----"

    def ret(self):
        self.mcdu.show(IndexPage)

class PreflightPage(Page):
    title = "ACARS PREFLIGHT"

    def init(self):
        self.field(0, "SYSTEM INIT", "<ARM", action=self.arm)
        self.field(0, "FLT NO", 7, format=Field.flightno, update=self.flightno)
        self.field(1, "ORIGIN", 4, format=Field.icao, update=self.origin)
        self.field(1, "PLAN DEP", 5, format=Field.time, update=self.plan_dep)
        self.field(2, "DEST", 4, format=Field.icao, update=self.dest)
        self.field(2, "ETA", 5,  format=Field.time, update=self.eta)
        self.field(3, "ALTRNT", -4, format=Field.icao, update=self.altrnt)
        self.field(3, "COMPANY", 3, format="^[A-Z]{3}$", update=self.company)
        self.field(4, "RECEIVED", "<MESSAGES", action=self.messages)
        self.field(4, "", "REQUESTS>", action=self.requests)
        self.field(5, "ACARS", "<INDEX", action=self.index)
        self.field(5, "", "INFLIGHT>", action=self.inflight)

    def arm(self):
        self.sys.avionics.reset()
        self.sys.armed = True
        self.field_update(0, 0, "ARMED")

    def flightno(self, value):
        self.sys.flightno = value

    def origin(self, value):
        self.sys.origin = value

    def plan_dep(self, value):
        self.sys.plan_dep = value

    def dest(self, value):
        self.sys.dest = value

    def eta(self, value):
        self.sys.eta = value

    def altrnt(self, value):
        self.sys.altrnt = value

    def company(self, value):
        self.sys.company = value

    def messages(self):
        self.mcdu.show(MessagesPage)

    def requests(self):
        self.mcdu.show(RequestsPage)

    def index(self):
        self.mcdu.show(IndexPage)

    def inflight(self):
        self.sys.state = ACARS.inflight
        self.mcdu.show(InflightPage)

class InflightPage(Page):
    title = "ACARS INFLIGHT"

    def init(self):
        self.field(0, "POSITION", "<REPORT", action=self.report)
        self.field(0, "ETA", self.sys.eta, format=Field.time, update=self.eta)
        self.field(1, "DEVIATE", self.sys.altrnt, format=Field.icao, update=self.deviate)
        self.field(4, "RECEIVED", "<MESSAGES", action=self.messages)
        self.field(4, "", "REQUESTS>", action=self.requests)
        self.field(5, "ACARS", "<INDEX", action=self.index)
        self.field(5, "", "POSTFLIGHT>", action=self.postflight)

    def report(self):
        self.sys.report()

    def eta(self, value):
        self.sys.eta = value

    def deviate(self, value):
        self.sys.altrnt = value

    def messages(self):
        self.mcdu.show(MessagesPage)

    def requests(self):
        self.mcdu.show(RequestsPage)

    def index(self):
        self.mcdu.show(IndexPage)

    def postflight(self):
        self.sys.state = ACARS.postflight
        self.mcdu.show(PostflightPage)

class PostflightPage(Page):
    title = "ACARS POSTFLIGHT"

    def init(self):
        pass

class MessagesPage(Page):
    title = "ACARS MESSAGES"

    def refresh(self):
        self.clear()

        messages = self.sys.messages
        for i in range(5):
            if i < len(messages):
                message = messages[i]
                self.field(i, message[0], message[2])
                self.field(i, "", message[1] + ">")

        self.field(5, "", "<RETURN", action=self.ret)
        Page.refresh(self)

    def lsk(self, pos):
        num, _ = pos

        if num < 5 and num < len(self.sys.messages):
            self.mcdu.show(MessagePage)
            self.mcdu.page.message = self.sys.messages[num]
            self.mcdu.page.refresh()
        else:
            Page.lsk(self, pos)

    def ret(self):
        self.sys.activate()

class MessagePage(Page):
    title = "ACARS MESSAGE"

    def init(self):
        self.message = None

    def refresh(self):
        self.clear()

        if self.message:
            text = textwrap.wrap(self.message[3], 24)

            for i in range(5):
                if i < len(text):
                    self.field(i, "", text[i])

        self.field(5, "", "<RETURN", action=self.ret)
        Page.refresh(self)

    def ret(self):
        self.mcdu.show(MessagesPage)

class RequestsPage(Page):
    title = "ACARS REQUESTS"

    def init(self):
        self.field(0, "", "<ROUTE", action=self.route)
        self.field(0, "", "WEATHER>", action=self.weather)
        self.field(1, "", "<RELEASE", action=self.release)
        self.field(1, "", "ATIS>", action=self.atis)
        self.field(2, "", "<LOADSHEET", action=self.loadsheet)
        self.field(3, "", "<ARR INFO", action=self.arr_info)
        self.field(4, "", "")
        self.field(4, "SEND", "TELEX>", action=self.telex)
        self.field(5, "", "<RETURN", action=self.ret)

    def route(self):
        pass

    def weather(self):
        self.mcdu.show(WeatherRequestPage)

    def release(self):
        pass

    def atis(self):
        pass

    def loadsheet(self):
        pass

    def arr_info(self):
        pass

    def telex(self):
        pass

    def ret(self):
        self.sys.activate()

class WeatherRequestPage(Page):
    title = "ACARS WEATHER REQUEST"

    def init(self):
        self.field(0, "Airport", 4, format=Field.icao, update=self.airport)
        self.field(3, "", "")
        self.field(3, "REQUEST", "METAR>", action=self.metar)
        self.field(4, "RECEIVED", "<MESSAGES", action=self.messages)
        self.field(4, "REQUEST", "TAF>", action=self.taf)
        self.field(5, "RETURN TO", "<REQUESTS", action=self.requests)
        self.field(5, "REQUEST", "SHORT TAF>", action=self.short_taf)

    def airport(self, value):
        self.apt = value

    def metar(self):
        self.sys.inforeq("metar", self.apt)

    def taf(self):
        self.sys.inforeq("taf", self.apt)

    def short_taf(self):
        self.sys.inforeq("shorttaf", self.apt)

    def requests(self):
        self.mcdu.show(RequestsPage)

    def messages(self):
        self.mcdu.show(MessagesPage)
