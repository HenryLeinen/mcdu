from subsystem import Subsystem
from page import Page, Field
from database import *
from helper import Longitude, Latitude
import math

class INIT(Subsystem):
    name = "INIT"

    def __init__(self, api):
        Subsystem.__init__(self)
        self.api = api
        self.CoRoute = ""
        self.fromAirport = ""
        self.toAirport = ""
        self.AltCoRoute = ""
        self.flightno = ""
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
        self.field(1, "ALTN", 4, format=Field.icao, update=self.update_AlternateAirport, mode=Field.optional)
        self.field(2, "FLT NBR", 7, format=Field.flightno, update=self.update_FlightNo)
        self.field(2, "", "ALIGN IRS>", action=self.show_alignIRS)
        self.field(3, "LAT", "----.--", mode=Field.optional)
        self.field(3, "LONG", "-----.--", mode=Field.optional)
        self.field(4, "COST INDEX", -3, update=self.update_CostIndex)
        self.field(4, "", "WIND>", action=self.show_wind)
        self.field(5, "CRZ FL/TEMP", (5,3), format=(Field.flightlevel, Field.temperature), update=self.update_CrzFlTemp, mode=Field.optional)
        self.field(5, "TROPO", str(self.sys.tropo), color=Field.blue, update=self.update_tropo)

    def update_CoRoute(self, value):
        self.sys.CoRoute = value
        # Also update all the other data

    def update_FromTo(self, value):
        self.sys.fromAirport = self.mcdu.database.findAirport(value[0])
        self.sys.toAirport = self.mcdu.database.findAirport(value[1])
        if not self.sys.fromAirport or not self.sys.toAirport:
            pass
        else:
            self.fields[5][0].mode = Field.mandatory
            self.fields[5][0].color = Field.orange
            self.fields[0][-1].color = Field.blue
            self.fields[3][0].color = Field.blue
            self.fields[3][-1].color = Field.blue
            self.update_latitude(self.sys.fromAirport.latitude)
            self.update_longitude(self.sys.fromAirport.longitude)
            self.field_update(0,0,"")
            self.field_update(1,0, "")
            self.field_update(5,0, u"\u25af"*5+"/"+u"\u25af"*3)

    def update_AlternateAirport(self, value):
        self.sys.altAirport = self.mcdu.database.findAirport(value)
        if self.sys.altAirport:
            self.sys.altAirport.dump()
            
    def update_latitude(self, value):
        self.latitude = '{0:02d}{1:02d}.{2:1d}{3:1s}'.format(value.degree, value.minute, value.second, value.sign)
        self.field_update(3, 0, self.latitude)

    def update_longitude(self, value):
        self.longitude = '{0:03d}{1:02d}.{2:1d}{3:1s}'.format(Longitude.getDegree(value), Longitude.getMinute(value), Longitude.getSecond(value), Longitude.getDirection(value))
        self.field_update(3, 1, self.longitude)

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
