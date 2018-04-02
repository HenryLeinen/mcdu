
from database import *


class FlightPlanLeg(object):

    def __init__(self, NavObj):
        self.ID = None
        self.nextLeg = 0
        self.object = NavObj

class FlightPlan(object):

    def __init__(self, fromApt, toApt):
        self.legs = [fromApt, toApt]

    def insertBefore(self, num, obj, link):
        if len(self.legs) > num and num > 0:
            self.legs = self.legs[:num-1] + obj + self.legs[num:]
            if link == True:
                self.legs[num-1].nextLeg = 1
            else:
                self.legs[num-1].nextLeg = 0

        else:
            raise Exception("invalid insert operation") 

