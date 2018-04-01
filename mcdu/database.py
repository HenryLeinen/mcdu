from helper import Latitude, Longitude

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

class Database(object):
    def __init__(self):
        self.id = ""
        with open("database/cycle_info.txt", "r") as file:
            for txt in file:
                if ':' in txt:
                    self.parseInfo(txt.split(':'))

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
        apt = ""
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


class Runway(object):
    title = "RUNWAY"
    def __init__(self, id, heading, length, ils_avail, ils_freq, ils_course, latitude, longitude, altitude, caps0, caps1):
        self.id = id
        self.heading = heading
        self.length = length
        self.ils_avail= ils_avail
        self.ils_freq = ils_freq
        self.ils_course = ils_course
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.caps0 = caps0
        self.caps1 = caps1

class Airport(object):
    title = "AIRPORT"
    def __init__(self, id, name, latitude, longitude, altitude):
        self.name = name
        self.id = id
        self.latitude = Latitude(latitude)
        self.longitude = Longitude(longitude)
        self.altitude = altitude
        self.runways = {}

    def addRunway(self, id, hdg, length, ils_avail, ils_freq, ils_course, latitude, longitude, altitude, caps0, caps1):
        self.runways[id] = Runway(id, hdg, length, ils_avail, ils_freq, ils_course, latitude, longitude, altitude, caps0, caps1)

    def dump(self):
        print ("Airport \"" + self.name + "\" ID:" + self.id + " has " + str(len(self.runways)) + " runways: ")

