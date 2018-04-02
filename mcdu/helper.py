# Helper functions
import math


class Latitude(object):
    Degree = 0
    Minute = 1
    Second = 2
    Direction = 3

    def __init__(self, latitude):
        self.latitude = latitude
        self.latitude_rad = latitude / 180.0 * math.pi
        if latitude >= 0:
            self.sign = 'N'
        else:
            self.sign = 'S'
            self.latitude = -self.latitude
        self.degree = int(math.floor(latitude))
        self.minute = int(math.floor((latitude - self.degree)*60))
        self.second = int(round(((latitude-self.degree)*60 - self.minute)*60))

    @staticmethod
    def getPart(value, part):
        if type(value)==str:
            value = float(value)
        elif type(value)==Latitude:
            value = value.latitude
        if value >= 0:
            sign = 'N'
        else:
            sign = 'S'
            value = -value
        degree = int(math.floor(value))
        minute = int(math.floor((value - degree)*60))
        second = int(round(((value-degree)*60 - minute)*60))
        if part == Latitude.Degree:
            return degree
        elif part == Latitude.Minute:
            return minute
        elif part == Latitude.Second:
            return second
        elif part == Latitude.Direction:
            return sign
    
    @staticmethod
    def getDirection(value):
        return Latitude.getPart(value, Latitude.Direction)

    @staticmethod
    def getSecond( value):
        return Latitude.getPart(value, Latitude.Second)

    @staticmethod
    def getMinute(value):
        return Latitude.getPart(value, Latitude.Minute)

    @staticmethod
    def getDegree(value):
        return Latitude.getPart(value, Latitude.Degree)



class Longitude(object):
    Degree = 0
    Minute = 1
    Second = 2
    Direction = 3

    def __init__(self, longitude):
        self.longitude = longitude
        self.longitude_rad = longitude / 180.0 * math.pi
        if longitude >= 0:
            self.sign = 'E'
        else:
            self.sign = 'W'
            longitude = -longitude
        self.degree = int(math.floor(longitude))
        self.minute = int(math.floor((longitude - self.degree)*60))
        self.second = int(round(((longitude-self.degree)*60 - self.minute)*60))

    def getLatitude(self):
        return self.longitude

    @staticmethod
    def getPart(value, part):
        if type(value)==str:
            value = float(value)
        elif type(value)==Longitude:
            value = value.longitude
        if value >= 0:
            sign = 'E'
        else:
            sign = 'W'
            value = -value
        degree = int(math.floor(value))
        minute = int(math.floor((value - degree)*60))
        second = int(round(((value-degree)*60 - minute)*60))
        if part == Longitude.Degree:
            return degree
        elif part == Longitude.Minute:
            return minute
        elif part == Longitude.Second:
            return second
        elif part == Longitude.Direction:
            return sign
    
    @staticmethod
    def getDirection(value):
        return Longitude.getPart(value, Longitude.Direction)

    @staticmethod
    def getSecond(value):
        return Longitude.getPart(value, Longitude.Second)

    @staticmethod
    def getMinute(value):
        return Longitude.getPart(value, Longitude.Minute)

    @staticmethod
    def getDegree(value):
        return Longitude.getPart(value, Longitude.Degree)


class TemperatureHelper(object):

    # Calculates the temperature at height <altitude_ft>, depending on the ground temperature <ground_temp_celsius> and
    # the height of the tropospere <tropo_ft>
    @staticmethod
    def getTemperature(ground_temp_celsius, altitude_ft, tropo_ft=36090):
        if altitude_ft > tropo_ft:
            temp = ground_temp_celsius - 0.0019812*tropo_ft 
        else:
            temp = ground_temp_celsius - 0.0019812*altitude_ft
        return temp

class SpeedHelper(object):

    # Calculates the speed of sound depending on the true outside air temperature in degrees celsius
    @staticmethod
    def getSoundSpeed(true_OAT_celsius):
        return 38.967854*math.sqrt(true_OAT_celsius+273.15)

    # Calculates the Mach number from indicated airspeed, and pressure altitude
    @staticmethod
    def getMach(ias_knots, pressure_altitude_ft):
        p_0 = 29.92126              # pressure under standard conditions in inch HG (corresponds to 1013.25 mB)
        CS_0 = 661.4786             # sound of speed in knots under  standard conditions (T=15 degrees C)
        P = p_0*(1.0-6.8755856*(10**-6)*pressure_altitude_ft)**5.2558797  
        DP = p_0*((1+0.2*(ias_knots/CS_0)**2)**3.5 - 1)
        M = (5*( (DP/P + 1)**(2/7)-1) ) ** 0.5
        return M
    