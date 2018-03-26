try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from urllib.error import URLError
except ImportError:
    from urllib import urlencode
    from urllib2 import URLError, urlopen

import re, time

API_URL = "http://www.hoppie.nl/acars/system/connect.html"
#API_URL = "http://10.0.0.11:8123/"

class ACARS_API(object):
    def __init__(self, logon):
        self.logon = logon
        self.messages = []

    def request(self, req_type, data={}):
        default_data = {
            "logon": self.logon,
            "to": "TEST",
            "type": req_type,
            "packet": "",
        }

        default_data.update(data)

        print(default_data)

        params = urlencode(default_data)
        path = "%s?%s" % (API_URL, params)

        try:
            res = urlopen(path)
        except URLError:
            return ""
        else:
            return res.read().decode("utf-8")

    def parse_data(self, data):
        if not data.startswith("ok") or len(data) < 3:
            return None

        regex = "\{([a-zA-Z0-9]+) ([a-z\-]+) \{(.*?)\}\}"

        for match in re.finditer(regex, data, re.DOTALL):
            # remove unnecessary whitespace
            msg_text = " ".join(match.group(3).split())
            message = (match.group(2), match.group(1), msg_text)
            self.messages_append(message)

    def messages_append(self, message):
        mtime = time.strftime("%H%MZ", time.gmtime())
        self.messages.append((message[0], mtime, message[1], message[2]))

    def poll(self, callsign):
        data = {
            "from": callsign,
            "to": "SERVER",
        }

        res = self.request("poll", data)
        self.parse_data(res)

    def poll_acars(self, callsign):
        self.poll(callsign)

        acars = []

        for message in self.messages:
            if message[0] in ["telex", "metar", "taf", "shorttaf"]:
                acars.append(message)
                self.messages.remove(message)

        return acars

    def poll_cpdlc(self, callsign):
        self.poll(callsign)

        cpdlc = []

        for message in self.messages:
            if message[0] == "cpdlc":
                cpdlc.append(message)
                self.messages.remove(message)

        return cpdlc

    def telex(self, callsign, receiver, message):
        data = {
            "from": callsign,
            "to": receiver,
            "packet": message,
        }
        self.request("telex", data)

    def cpdlc(self, callsign, receiver, message):
        data = {
            "from": callsign,
            "to": receiver,
            "packet": message,
        }
        self.request("cpdlc", data)

    def progress(self, callsign, receiver, message):
        data = {
            "from": callsign,
            "to": receiver,
            "packet": message,
        }
        self.request("progress", data)

    def inforeq(self, callsign, req, apt):
        data = {
            "from": callsign,
            "to": "SERVER",
            "packet": "%s %s" % (req, apt)
        }
        resp = self.request("inforeq", data)

        regex = "^ok \{server info \{(.*)\}\}"
        match = re.match(regex, resp)

        if (match):
            mtime = time.strftime("%H%MZ", time.gmtime())
            msg = (req, mtime, apt, match.group(1))
            self.messages.append(msg)
