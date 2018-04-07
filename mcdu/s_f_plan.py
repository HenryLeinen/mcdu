from mcdu.subsystem import Subsystem
from mcdu.page import Page, Field
from mcdu.database import NavObject

class FPLAN(Subsystem):
    name = "F_PLN"

    def __init__(self, api):
        Subsystem.__init__(self)
        self.api = api

    def activate(self):
        self.mcdu.show(FPlanPage1)
        self.activePage = 1

    def next_page(self):
        if self.activePage == 2:
            self.mcdu.show(FPlanPage1)
            self.activePage = 1
        else:
            self.mcdu.show(FPlanPage2)
            self.activePage = 2


class FPlanPage1(Page):
    title = "FROM"
    
    def init(self):
        self.offset = 0

    def refresh(self):
        self.clear()
        name, time, speed, alt, clr = self.getItem(0)
        self.field(0, "FROM                    TIME", name + "     " +time, color=clr)
        self.field(0, "SPD/ALT                ", speed + "/" + alt, color = clr)
        for i in range (1, 5):
            name, time, speed, alt, clr = self.getItem(i)
            self.field(i, "", name + "     " + time, color = clr) 
            if speed == "" and alt == "":
                self.field(i, "", "")
            else:
                self.field(i, "", speed + "/" + alt, color= clr)
        Page.refresh(self)
        
    def getItem(self, i):
        n = i + self.offset
        leg = self.mcdu.flightplan.getLeg(n)
        if not leg:
            if self.mcdu.flightplan.getNumberOfLegs() == n:
                # show the 'end of flightplan'
                return ("----------- END OF F-PLAN -----------", "", "", "", Field.white)
            else:
                return ("", "", "", "", Field.white)
        else:
            name = leg.object.getID()
            if leg.time == 0:
                time = "----"
            else:
                time = str (leg.time)
            if leg.speed == 0:
                speed = "---"
            else:
                speed = str (leg.speed)
            if leg.altitude == 0:
                alt = "-----"
            elif leg.altitude < 18000:
                alt = str(leg.altitude)
            else:
                alt = "FL" + str(leg.altitude/100)
            if leg.object.nav_object_type == NavObject.AIRPORT:
                clr = Field.green
            else:
                clr = Field.white
        return (name, time, speed, alt, clr)
                

class FPlanPage2(Page):

    def init(self):
        pass
