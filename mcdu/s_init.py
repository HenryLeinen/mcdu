from mcdu.subsystem import Subsystem
from mcdu.page import Page, Field
from mcdu.database import Database, Airport, Waypoint, Runway
from mcdu.helper import Longitude, Latitude
from mcdu.flightplan import FlightPlan
import math


class Wind(object):

    def __init__(self, value):
        d, k, h = value
        self.dir = int(d)
        self.knots = int(k)
        self.height = int(h)

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
        self.climbWinds = []
        self.cruiseWinds = []
        self.descendWinds = []

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
        self.mcdu.flightplan = FlightPlan(self.sys.fromAirport, self.sys.toAirport)
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
            dist = self.sys.fromAirport.distanceToObject(self.sys.toAirport)
            print ("Distance between ",self.sys.fromAirport.getID() , " and " , self.sys.toAirport.getID() , " is :" , dist, "nm")
            crs = self.sys.fromAirport.courseToObject(self.sys.toAirport)
            print ("Course from ", self.sys.fromAirport.getID(), " and ", self.sys.toAirport.getID(), " is ", crs)

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
        self.field(0, "TRU WIND/ALT", "", convert=(Field.convertToHeading, None, Field.convertAltitudeToFlightLevel), format=(Field.heading, Field.speedknots, Field.flightlevel), update=self.on_update_wind0)
        self.field(0, "HISTORY", "WIND>", action=self.show_history)
        self.field(1, "", "", convert=(Field.convertToHeading, None, Field.convertAltitudeToFlightLevel), format=(Field.heading, Field.speedknots, Field.flightlevel), update=self.on_update_wind1)
        self.field(1, "WIND", "REQUEST*", action=self.wind_request)
        self.field(2, "", "", convert=(Field.convertToHeading, None, Field.convertAltitudeToFlightLevel), format=(Field.heading, Field.speedknots, Field.flightlevel), update=self.on_update_wind2)
        self.field(3, "", "", convert=(Field.convertToHeading, None, Field.convertAltitudeToFlightLevel), format=(Field.heading, Field.speedknots, Field.flightlevel), update=self.on_update_wind3)
        self.field(4, "", "", convert=(Field.convertToHeading, None, Field.convertAltitudeToFlightLevel), format=(Field.heading, Field.speedknots, Field.flightlevel), update=self.on_update_wind4)
        self.field(4, "", "NEXT PHASE>", action=self.show_nextphase)
        self.field(5, "", "<RETURN", action=self.show_return)

    def refresh(self):
        # Only show
#        self.clear()
        print ("Refreshing page !")
        j = 0
        n = len(self.sys.climbWinds) 
        for i in range(n):
            item = u"{0:03d}\u00b0/{1:03d}/{2:5d}".format(self.sys.climbWinds[i].dir, self.sys.climbWinds[i].knots, self.sys.climbWinds[i].height)
            self.field_update(i, 0, item)
            j += 1
        print ("Updating field ", j)
        self.field_update(j, 0, u"[   ]\u00b0/[   ]/[     ]")
        Page.refresh(self)

    def on_update_wind0(self, value):
        if len(self.sys.climbWinds) == 0:
            self.sys.climbWinds.append(Wind(value))
        else:
            self.sys.climbWinds[0] = Wind(value)
        self.refresh()

    def on_update_wind1(self, value):
        if len(self.sys.climbWinds) == 1:
            self.sys.climbWinds.append(Wind(value))
        else:
            self.sys.climbWinds[1] = Wind(value)
        self.refresh()

    def on_update_wind2(self, value):
        pass

    def on_update_wind3(self, value):
        pass

    def on_update_wind4(self, value):
        pass

    def show_nextphase(self):
        self.mcdu.show(CruiseWindPage)

    def show_return(self):
        self.sys.activate()

    def show_history(self):
        pass

    def wind_request(self):
        pass

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
