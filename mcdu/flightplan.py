
from database import *


class FlightPlanLeg(object):

    def __init__(self, NavObj):
        self.ID = None
        self.nextLeg = 0
        self.object = NavObj
        self.altitude = 0
        self.speed = 0
        self.heading = 0
        self.time = 0

class FlightPlan(object):

    def __init__(self, fromApt, toApt):
        self.legs = [FlightPlanLeg(fromApt), FlightPlanLeg(toApt)]

    def insertBefore(self, num, obj, link):
        if len(self.legs) > num and num > 0:
            self.legs = self.legs[:num-1] + obj + self.legs[num:]
            if link == True:
                self.legs[num-1].nextLeg = 1
            else:
                self.legs[num-1].nextLeg = 0

        else:
            raise Exception("invalid insert operation") 


    def getLeg(self, i):
        if not self.legs:
            return None
        elif len(self.legs) > i:
            return self.legs[i]
        else:
            return None

    def getNumberOfLegs(self):
        if not self.legs:
            return 0
        else:
            return len(self.legs)