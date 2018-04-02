from mcdu.helper import Latitude, Longitude
import math

# Implements the database provider
# The current implementation uses X-FMC data, which can be obtained from navigraph.
# The database files are expected to be stored in the subfolder $(MCDU_MAIN)/database
#
# The X-FMC database consists of text files which contain different information:
#   cycle-info.txt      contains information about the dataset
#   airports.txt        lists all airports and runways
#   ats.txt
#   navaids.txt
#   waypoints.txt

def degreesToRadian(deg):
    return deg/180.0*math.pi

def radianToDegrees(rad):
    return rad/math.pi*180.0

class NavObject(object):
    AIRPORT = 1
    RUNWAY = 2
    ILS = 3
    ILSDME = 4
    VOR = 5
    VORDME = 6
    DME = 7
    NDB = 8
    WAYPOINT = 9
    Other = -1

    def __init__(self, ident, latitude, longitude, nav_object_type):
        self.ident = ident
        self.latitude = Latitude(latitude)
        self.longitude = Longitude(longitude)
        self.nav_object_type = nav_object_type

    def radianDistanceTo(self, lat, lon):
        lat_rad= lat.latitude_rad
        lon_rad = lon.longitude_rad
        my_lat_rad = self.latitude.latitude_rad
        my_lon_rad = self.longitude.longitude_rad
        sd = 2*math.asin(math.sqrt((math.sin((lat_rad-my_lat_rad)/2))**2 + math.cos(lat_rad)*math.cos(my_lat_rad)*(math.sin((lon_rad-my_lon_rad)/2))**2))
        return sd

    def distanceTo(self, lat, lon):
        return 180*60/math.pi*self.radianDistanceTo(lat, lon)

    def radianCourseTo(self, lat, lon):
        lat2 = lat.latitude_rad
        lon2 = lon.longitude_rad
        lat1 = self.latitude.latitude_rad
        lon1 = self.longitude.longitude_rad
        if math.cos(lat1) < 0.00000001:
            if lat1 > 0:
                crs = math.pi
            else:
                crs = 2*math.pi
        else:
            d = self.radianDistanceTo(lat, lon)        
            crs = math.acos((math.sin(lat2)-math.sin(lat1)*math.cos(d))/(math.sin(d)*math.cos(lat1)))
            if math.sin(lon2-lon1) < 0:
                crs = 2*math.pi - crs

        return crs

    def courseTo(self, lat, lon):
        return radianToDegrees(self.radianCourseTo(lat, lon))

    def distanceToObject(self, no):
        print ("NavObject: Calculating distance to object " + no.name)
        if type(no)==NavObject or type(no) == Airport or type(no) == Runway or type(no) == Waypoint:
            return self.distanceTo(no.latitude, no.longitude)
        else:
            raise Exception("Unknown type")
        return 0

    def courseToObject(self, no):
        print ("NavObject: Calculating course to object " + no.name)
        if type(no)== NavObject or type(no) == Airport or type(no) == Runway or type(no) == Waypoint:
            return self.courseTo(no.latitude, no.longitude)
        else:
            raise Exception("Unknown type")


    def getID(self):
        return self.ident

    def getLatitude(self):
        return self.latitude

    def getLongitude(self):
        return self.longitude

class Runway(NavObject):
    title = "RUNWAY"
    def __init__(self, id, heading, length, ils_avail, ils_freq, ils_course, latitude, longitude, altitude, caps0, caps1):
        NavObject.__init__(self, id, latitude, longitude, NavObject.RUNWAY)
#        self.id = id
        self.heading = heading
        self.length = length
        self.ils_avail= ils_avail
        self.ils_freq = ils_freq
        self.ils_course = ils_course
#        self.latitude = latitude
#        self.longitude = longitude
        self.altitude = altitude
        self.caps0 = caps0
        self.caps1 = caps1


    def getID(self):
        return super(Runway, self).getID()

    def getLatitude(self):
        return super(Runway, self).getLatitude()

    def getLongitude(self):
        return super(Runway, self).getLongitude()



class Airport(NavObject):

    title = "AIRPORT"

    def __init__(self, id, name, latitude, longitude, altitude):
        NavObject.__init__(self, id, latitude, longitude, NavObject.AIRPORT)
        self.name = name
        self.altitude = altitude
        self.runways = {}

    def addRunway(self, id, hdg, length, ils_avail, ils_freq, ils_course, latitude, longitude, altitude, caps0, caps1):
        self.runways[id] = Runway(id, hdg, length, ils_avail, ils_freq, ils_course, latitude, longitude, altitude, caps0, caps1)

    def dump(self):
        print ("Airport \"" + self.name + "\" ID:" + super().getID() + " has " + str(len(self.runways)) + " runways: ")

#    def getID(self):
#        return super().getID()

#    def getLatitude(self):
#        return super().getLatitude()

#    def getLongitude(self):
#        return super().getLongitude()

#    def distanceToObject(self, no):
#        print ("Airpot: Calculate distance to object " + no.name)
#        return super().distanceToObject(no)

class Navaid(NavObject):

    title = "NAVAID"

    def __init__(self, id, name, latitude, longitude, freq, hasVOR, hasDME, hasNDB, hasILS, elevation, magn_vari):
        t = NavObject.Other
        if hasVOR == True:
            if hasDME == True:
                t = NavObject.VORDME
            else:
                t = NavObject.VOR
        elif hasNDB == True:
                t = NavObject.NDB
        elif hasILS == True:
            if hasDME == True:
                t = NavObject.ILSDME
            else:
                t = NavObject.ILS
        elif hasDME == True:
            t = NavObject.DME
        NavObject.__init__(self, id, latitude, longitude, t)
        self.name = name
        self.elevation = elevation
        self.frequency = freq
        self.magnetic_variation = magn_vari

    
    def getID(self):
        return super(Navaid, self).getID()

    def getLatitude(self):
        return super(Navaid, self).getLatitude()

    def getLongitude(self):
        return super(Navaid, self).getLongitude()


class Waypoint(NavObject):

    title = "WAYPOINT"

    def __init__(self, id, latitude, longitude):
        NavObject.__init__(self, id, latitude, longitude, NavObject.WAYPOINT)

    def getID(self):
        return super(Waypoint, self).getID()

    def getLatitude(self):
        return super(Waypoint, self).getLatitude()

    def getLongitude(self):
        return super(Waypoint, self).getLongitude()


class Database(object):
    def __init__(self):
        self.id = ""
        with open("database/cycle_info.txt", "r") as file:
            for txt in file:
                if ':' in txt:
                    self.parseInfo(txt.split(':'))
        print ("Loading NAVAIDS...")
#        self.loadNavAids()
        print ("Loading AIRPORTS...")
#        self.loadAirports()
        print ("Loading WAYPOINTS...")
#        self.loadWaypoints()

    def parseInfo(self, lst):
        if lst[0][:11] == "AIRAC cycle":
            self.cycle = lst[1].split()[0]
        elif lst[0][:7] == "Version":
            self.version = lst[1].split()[0]
        elif lst[0][:5] == "Valid":
            dr = lst[1].split('-')
            self.validityFrom =dr[0].split('/')
            self.validityTo   =dr[1].split('/')

    def getId(self):
        if not self.cycle or not self.version or not self.validityTo:
            return "NONE"
        else:
            return self.validityFrom[0]+self.validityFrom[1]+"-"+self.validityTo[0]+self.validityTo[1] + "   " + self.cycle + "[" + self.version + "]"

    def findAirport(self, airport):
        apt = None
        l = 0
        a = 0
        state = 1
#        print ("Finding airport with ID: " + airport)
        with open("database/airports.txt", "r") as file:
            file.seek(0)
            for txt in file:
                l+=1
                if state == 1:  # search airport
                    if txt[0]=='A':
                        a+=1
                        apts = txt.split('|')
                        if apts[1] == airport:
                            lat = float(apts[3])
                            lat /= 1000000.0
                            lon = float(apts[4])
                            lon /= 1000000.0
                            apt = Airport(apts[1], apts[2], lat, lon, apts[5])
                            state = 2
                elif state == 2:   # add runways
                    if txt[0]== 'R':
                        rwys = txt.split('|')
                        lat = float(rwys[7])
                        lat /= 1000000.0
                        lon = float(rwys[8])
                        lon /= 1000000.0
                        apt.addRunway(rwys[1], rwys[2], rwys[3], rwys[4], rwys[5], rwys[6], lat, lon, rwys[9], rwys[10], rwys[11])
                    else:
                        return apt
        print ("Airport with ID: " + airport + " not found !!!")
        print (list(airport))
        print ("searched through " + str(l) + " lines, while identified " + str(a) + " airport entries !")
        return apt

    def loadAirports(self):
        apt = None
        self.airports = {}
        l = 0
        a = 0
        state = 1
        with open("database/airports.txt", "r") as file:
            file.seek(0)
            for txt in file:
                l+=1
                if state == 1:  # search airport
                    if txt[0]=='A':
                        a+=1
                        apts = txt.split('|')
                        lat = float(apts[3])
                        lat /= 1000000.0
                        lon = float(apts[4])
                        lon /= 1000000.0
                        apt = Airport(apts[1], apts[2], lat, lon, apts[5])
                        state = 2
                elif state == 2:   # add runways
                    if txt[0]== 'R':
                        rwys = txt.split('|')
                        lat = float(rwys[7])
                        lat /= 1000000.0
                        lon = float(rwys[8])
                        lon /= 1000000.0
                        apt.addRunway(rwys[1], rwys[2], rwys[3], rwys[4], rwys[5], rwys[6], lat, lon, rwys[9], rwys[10], rwys[11])
                    else:
                        self.airports[apt.ID] = apt
                        state = 1
        print ("Found " + str(a) + " Airports.")

    def loadNavAids(self):
        nvd = None
        self.navaids = {}
        n = 0
        with open("database/navaids.txt", "r") as file:
            file.seek(0)
            for txt in file:
                n+=1
                nvds = txt.split('|')
                id = nvds[0]
                name = nvds[1]
                freq = float(nvds[2])
                freq /= 1000.0
                isVOR = nvds[3]
                isDME = nvds[4]
                if isVOR == 0:
                    isNDB = 1
                else:
                    isNDB = 0
                unknown = nvds[5]
                if unknown != "195":
                    print ("Strange navaid found !")
                lat = float(nvds[6])
                lat /= 1000000.0
                lon = float(nvds[7])
                lon /= 1000000.0
                elev = nvds[8]
#                cntry = nvds[9]
                nvd = Navaid(id, name, lat, lon, isVOR, isDME, isNDB, 0, elev, 0, 0)
                self.navaids[nvd.getID()] = nvd
        print ("Found " + str(n) + " NavAids.")


    def loadWaypoints(self):
        wpt = None
        self.waypoints = {}
        w = 0
        with open("database/waypoints.txt", "r") as file:
            file.seek(0)
            for txt in file:
                w+=1
                wpts = txt.split('|')
                id = wpts[0]
                lat = float(wpts[1])
                lat /= 1000000.0
                lon = float(wpts[2])
                lon /= 1000000.0
#                cntry = wpts[3]
                wpt = Waypoint(id, lat, lon)
                self.waypoints[wpt.getID()] = wpt
        print ("Found " + str(w) + " Waypoints.")
