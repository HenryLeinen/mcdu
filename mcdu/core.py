from mcdu.page import Page

class MCDU():
    def __init__(self):
        self.sys = None
        self.page = None
        self.subsystems = []
        self.displays = []
        self.scratch = ""

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

    def show(self, page):
        """Switch to the given page."""
        self.page = page(self, self.sys)
        self.page.refresh()

    def lsk(self, pos):
        """Forward the pressed Line Select Key to the page."""
        if self.page: self.page.lsk(pos)

    def scratch_input(self, text):
        """Append a string to the scratchpad."""
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
        num, side = pos

        if num < len(self.mcdu.subsystems):
            sys = self.mcdu.subsystems[num]
            self.mcdu.subsystem_activate(sys)
