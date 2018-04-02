#!/usr/bin/env python

from mcdu.core import MCDU
from mcdu.acars import ACARS
from mcdu.atc import ATC
from mcdu.network import ACARS_API
from mcdu.display import myDisplay
from mcdu.s_data import DATA
from mcdu.s_init import INIT
from mcdu.database import Database

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
        print("no simulator set")
        return 1

    db = Database()
    receiver.start()

    api = ACARS_API(config.get("ACARS", "logon"))
    acars = ACARS(api)
    atc = ATC(api)
    data = DATA(api)
    init = INIT(api)

    mcdu = MCDU()
    mcdu.subsystem_register(acars)
    mcdu.subsystem_register(atc)
    mcdu.subsystem_register(data)
    mcdu.subsystem_register(init)
    mcdu.database_register(db)
    mcdu.menu()

    application = myDisplay()

    port = config.getint("General", "port")

    application.initialize(mcdu)
    application.open()

    try:
        print("running on port %i" % port)
	    # Call my application here
        application.mainloop()
#        receiver.run()
    except KeyboardInterrupt:
        print("quitting...")
    except Exception:
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
