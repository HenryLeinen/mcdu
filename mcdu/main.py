#!/usr/bin/env python

from mcdu.core import MCDU
from mcdu.acars import ACARS
from mcdu.atc import ATC
from mcdu.network import ACARS_API
from display import myDisplay
#from mcdu.websocket import WebSocket

#import tornado.ioloop
#import tornado.web

import os, sys

try:
    from configparser import SafeConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser

def run():
    config = SafeConfigParser()
    config.read("config/defaults.cfg")
    config.read("~/.config/mcdu.cfg")
    config.read("config/mcdu.cfg")

    sim = config.get("General", "sim")
    if sim == "fsx":
        from mcdu.fsx import FSXReceiver
        receiver = FSXReceiver()
    elif sim == "xplane":
        from mcdu.xplane import XPlaneReceiver
        receiver = XPlaneReceiver()
    else:
        print("no simulator set");
        return 1

    receiver.start()

    api = ACARS_API(config.get("ACARS", "logon"))
    acars = ACARS(api)
    atc = ATC(api)

    mcdu = MCDU()
    mcdu.subsystem_register(acars)
    mcdu.subsystem_register(atc)
    mcdu.menu()

    application = myDisplay()
#    application = tornado.web.Application([
#        (r"^/socket", WebSocket, dict(mcdu=mcdu)),
#        (r"^/(.*)$", tornado.web.StaticFileHandler, {"path": "res/", "default_filename": "index.html"}),
#    ], debug=False)

    port = config.getint("General", "port")
#    application.listen(port)

    application.initialize(mcdu)
    application.open()

    try:
        print("running on port %i" % port)
	# Call my application here
	application.mainloop()
    except KeyboardInterrupt:
        print("quitting...")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("quitting...")
    finally:
        receiver.stop()
        acars.stop()
        atc.stop()
        return 0

if __name__ == "__main__":
	r = run()
	sys.exit(r)
