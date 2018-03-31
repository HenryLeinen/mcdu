from subsystem import Subsystem
from page import Page, Field
from database import *
import math

class INIT(Subsystem):
    name = "INIT"

    def __init__(self, api):
        Subsystem.__init__(self)
        self.api = api
        self.CoRoute = ""
        self.fromto = ""
        self.AltCoRoute = ""
        self.flightno = ""
        self.position = (45.781111, 108.5038888)
        self.costindex = ""
        self.tropo = 36090

    def activate(self):
        self.mcdu.show(InitIndexPage1)
        self.activePage = 1

    def next_page(self):
        if self.activePage == 2:
            self.mcdu.show(InitIndexPage1)
            self.activePage = 1
        else:
            self.mcdu.show(InitIndexPage2)
            self.activePage = 2

class InitIndexPage1(Page):
    title = "INIT   <->"

    def init(self):
        self.field(0, "CO RTE", 10, format=Field.coroute, update=self.update_CoRoute, mode=Field.mandatory)
        self.field(0, "FROM/TO", (4,4), format=(Field.icao, Field.icao), update=self.update_FromTo, mode=Field.mandatory)
        self.field(1, "ALTN/CO RTE", 10, format=Field.coroute, update=self.update_AltCoRoute)
        self.field(2, "FLT NBR", 7, format=Field.flightno, update=self.update_FlightNo)
        self.field(2, "", "ALIGN IRS>", action=self.show_alignIRS)
        self.field(3, "LAT", '{0:04d}.{1:1d}'.format(int(math.floor(self.sys.position[0]*100)), int(10*(self.sys.position[0]*100-math.floor(self.sys.position[0]*100)))))
        self.field(3, "LONG", '{0:05d}.{1:1d}'.format(int(math.floor(self.sys.position[1])), 10*int(self.sys.position[1]-math.floor(self.sys.position[1]))))
        self.field(4, "COST INDEX", 3, update=self.update_CostIndex)
        self.field(4, "", "WIND>", action=self.show_wind)
        self.field(5, "CRZ FL/TEMP", (5,3), format=(Field.flightlevel, Field.temperature), update=self.update_CrzFlTemp, mode=Field.optional)
        self.field(5, "TROPO", str(self.sys.tropo), color=Field.blue, update=self.update_tropo)

    def update_CoRoute(self, value):
        self.sys.CoRoute = value
        # Also update all the other data

    def update_FromTo(self, value):
        self.sys.fromto = value
        aptFrom = self.mcdu.database.findAirport(value[0])
        aptTo = self.mcdu.database.findAirport(value[1])
        if aptFrom:
            aptFrom.dump()
        if aptTo:
            aptTo.dump()

    def update_AltCoRoute(self, value):
        self.sys.AltCoRoute = value

    def update_FlightNo(self, value):
        self.sys.flightno = value

    def show_alignIRS(self):
        pass

    def update_CostIndex(self, value):
        self.sys.costindex = value

    def show_wind(self):
        self.mcdu.show(ClimbWindPage)

    def update_CrzFlTemp(self, value):
        self.sys.crzFlTemp = value

    def update_tropo(self, value):
        self.sys.tropo = value

class InitIndexPage2(Page):
    title = "INIT   <->"

    def init(self):
        pass

class ClimbWindPage(Page):
    title = "CLIMB WIND"

    def init(self):
        self.field(0, "TRU WIND/ALT", "")
        self.field(4, "", "")
        self.field(4, "", "NEXT PHASE>", action=self.show_nextphase)
        self.field(5, "", "<RETURN", action=self.show_return)

    def show_nextphase(self):
        self.mcdu.show(CruiseWindPage)

    def show_return(self):
        self.sys.activate()

class CruiseWindPage(Page):
    title = "CRUISE WIND"

    def init(self):
        self.field(0, "TRU WIND/ALT", "")
        self.field(3, "", "")
        self.field(3, "", "PREV PHASE>", action=self.show_prevphase)
        self.field(4, "", "")
        self.field(4, "", "NEXT PHASE>", action=self.show_nextphase)
        self.field(5, "", "<RETURN", action=self.show_return)

    def show_prevphase(self):
        self.mcdu.show(ClimbWindPage)

    def show_nextphase(self):
        self.mcdu.show(DescendWindPage)

    def show_return(self):
        self.sys.activate()

class DescendWindPage(Page):
    title = "DESCEND WIND"

    def init(self):
        self.field(0, "TRU WIND/ALT", "")
        self.field(3, "", "")
        self.field(3, "", "PREV PHASE>", action=self.show_prevphase)
        self.field(5, "", "<RETURN", action=self.show_return) 

    def show_prevphase(self):
        self.mcdu.show(CruiseWindPage)

    def show_return(self):
        self.sys.activate()
