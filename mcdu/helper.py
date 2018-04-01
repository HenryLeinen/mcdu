# Helper functions
import math


class Latitude(object):
    Degree = 0
    Minute = 1
    Second = 2
    Direction = 3

    def __init__(self, latitude):
        self.latitude = latitude
        if latitude >= 0:
            self.sign = 'N'
        else:
            self.sign = 'S'
            self.latitude = -self.latitude
        self.degree = int(math.floor(latitude))
        self.minute = int(math.floor((latitude - self.degree)*60))
        self.second = int(round(((latitude-self.degree)*60 - self.minute)*60))

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
    
    def getDirection(value):
        return Latitude.getPart(value, Latitude.Direction)

    def getSecond( value):
        return Latitude.getPart(value, Latitude.Second)

    def getMinute(value):
        return Latitude.getPart(value, Latitude.Minute)

    def getDegree(value):
        return Latitude.getPart(value, Latitude.Degree)



class Longitude(object):
    Degree = 0
    Minute = 1
    Second = 2
    Direction = 3

    def __init__(self, longitude):
        self.longitude = longitude
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
    
    def getDirection(value):
        return Longitude.getPart(value, Longitude.Direction)

    def getSecond(value):
        return Longitude.getPart(value, Longitude.Second)

    def getMinute(value):
        return Longitude.getPart(value, Longitude.Minute)

    def getDegree(value):
        return Longitude.getPart(value, Longitude.Degree)

