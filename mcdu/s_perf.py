from mcdu.page import Page,Field
from mcdu.subsystem import Subsystem

class PERF(Subsystem):
    name = "PERF"

    def __init__(self, api):
        Subsystem.__init__(self)
        self.api = api
        self.V1 = 0
        self.VR = 0
        self.V2 = 0
        self.Flaps = 157
        self.Slats = 203
        self.takeoff_shift= "  "
        self.Runway = "33L"
        self.TransitionAltitude = 4800

    def activate(self):
        self.mcdu.show(PerfTakeOffPage)


class PerfTakeOffPage(Page):
    title = "TAKE OFF"

    def init(self):
        self.field(0, "V1", 3, format=Field.speedknots, mode=Field.mandatory, update=self.on_update_V1)
        self.field(0, "FLP RETR                       RWY", "F="+str(self.sys.Flaps)+ "       "+self.sys.Runway )
        self.field(1, "VR", 3, format=Field.speedknots, mode=Field.mandatory, update=self.on_update_VR)
        self.field(1, "SLT RETR                 TO SHIFT", "S="+str(self.sys.Slats)+ "   [M]["+self.sys.takeoff_shift+"]")
        self.field(2, "V2", 3, format=Field.speedknots, mode=Field.mandatory, update=self.on_update_V2)
        self.field(2, "CLEAN                   FLAPS/THS", "[  ]/[  ]")
        self.field(3, "TRANS ALT", str(self.sys.TransitionAltitude))
        self.field(3, "FLEX TO TEMP", u"[  ]\u00b0")
        self.field(4, "THR RED/ACC", "2000/3000")
        self.field(4, "ENG OUT ACC", "2265")
        self.field(5, "UPLINK", "< TO DATA")
        self.field(5, "NEXT", "PHASE>", action=self.next_page)

    def on_update_V1(self, value):
        self.sys.V1 = value

    def on_update_VR(self, value):
        self.sys.VR = value

    def on_update_V2(self, value):
        self.sys.V2 = value

    def next_page(self):
        pass
class PerfClimbPage(Page):
    title = "CLIMB"

    def init(self):
        pass

class PerfCruizePage(Page):
    title = "CRUISE"

    def init(self):
        pass

class PerfDescendPage(Page):
    title = "DESCEND"

    def init(self):
        pass


class PerfApproachPage(Page):
    title = "APPROACH"

    def init(self):
        pass


class PerfGoAroundPage(Page):
    title = "GO AROUND"

    def init(self):
        pass


class PerfClbApprPage(Page):
    title = "CLB/APPR"

    def init(self):
        pass