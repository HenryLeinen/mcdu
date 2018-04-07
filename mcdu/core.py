from mcdu.page import Page
from mcdu.database import Database
from mcdu.flightplan import FlightPlan

class MCDU():
    FP_PREFLIGHT = 1
    FP_TAKEOFF = 2
    FP_CLIMB = 3
    FP_CRUISE = 4
    FP_DESCENT = 5
    FP_APPROACH = 6
    FP_GO_AROUND = 7
    FP_DONE = 0

    def __init__(self):
        self.sys = None
        self.page = None
        self.subsystems = []
        self.displays = []
        self.scratch = ""
        self.database = None
        self.flightplan = None

    def database_register(self, database):
        """Register database, eventually pre load data"""
        self.database = database

    def subsystem_register(self, subsystem):
        """Register and start the given subsystem."""
        self.subsystems.append(subsystem)
        subsystem.connect(self)
        subsystem.start()

    def subsystem_activate(self, subsystem):
        """Activate the given subsystem."""
        self.sys = subsystem
        subsystem.activate()

    def menu(self):
        """Show the menu page."""
        self.show(MenuPage)

    def dir(self):
        """Show the dir page."""
#        print "TBD: DIR handling"
        pass

    def prog(self):
        """Show the prog page."""
#        print "TBD: PROG handling"
        pass

    def perf(self):
        """Show the perf page."""
#        print "TBD: PERF handling"
        pass

    def init(self):
        """Show the init page."""
#        print "TBD: INIT handling"
        for s in self.subsystems:
            if s.name == "INIT":
                self.subsystem_activate(s)
        pass

    def data(self):
        """Show the data page."""
#        print "TBD: DATA handling"
        for s in self.subsystems:
            if s.name == "DATA":
                self.subsystem_activate(s)
        pass

    def f_pln(self):
        """Show the flightplan page."""
#        print "TBD: F_PLN handling"
        for s in self.subsystems:
            if s.name == "F_PLN":
                self.subsystem_activate(s)
        pass

    def rad_nav(self):
        """Show the rad_nav page."""
#        print "TBD: RAD_NAV handling"
        pass

    def airport(self):
        """Show the airport page."""
#        print "TBD: AIRPORT handling"
        pass

    def next_page(self):
        """Show the next page."""
        self.sys.next_page()

    def show(self, page):
        """Switch to the given page."""
        self.page = page(self, self.sys)
        self.page.refresh()

    def lsk(self, pos):
        """Forward the pressed Line Select Key to the page."""
        if self.page: self.page.lsk(pos)

    def scratch_input(self, text):
        """Append a string to the scratchpad."""
        if text == "+" and len(self.scratch) >0 and self.scratch[-1] == "+":
            self.scratch = self.scratch[:-1] + "-"
        else:
            self.scratch += text
        self.scratch_update()

    def scratch_set(self, text):
        """Change the scratchpad to the given string."""
        self.scratch = text
        self.scratch_update()

    def scratch_delete(self):
        """Delete the last character of the scratchpad."""
        if len(self.scratch) > 0:
            self.scratch = self.scratch[:-1]
            self.scratch_update()

    def scratch_clear(self):
        """Clear the scratchpad."""
        self.scratch_set("")

    def scratch_text(self):
        if (len(self.scratch) > 24):
            return "<" + self.scratch[-23:]
        else:
            return self.scratch

    def scratch_update(self):
        for display in self.displays:
            display.update_scratch()

    def update_row(self, index):
        if not self.page: return
        for display in self.displays:
            display.update_row(index)

    def update(self):
        if not self.page: return
        for display in self.displays:
            display.update()

    def add_display(self, display):
        self.displays.append(display)
        self.update()

    def remove_display(self, display):
        self.displays.remove(display)

class MenuPage(Page):
    title = "MCDU MENU"

    def init(self):
        for i in range(len(self.mcdu.subsystems)):
            subsystem = self.mcdu.subsystems[i]
            self.field(i, "", "<" + subsystem.name)

    def lsk(self, pos):
        num, _ = pos

        if num < len(self.mcdu.subsystems):
            sys = self.mcdu.subsystems[num]
            self.mcdu.subsystem_activate(sys)
