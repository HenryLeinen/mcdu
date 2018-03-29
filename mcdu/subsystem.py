import threading

class Subsystem(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def connect(self, mcdu):
        self.running = True
        self.mcdu = mcdu

    def refresh(self):
        if self.mcdu and self.mcdu.sys == self:
            self.mcdu.page.refresh()

    def stop(self):
        self.running = False

    def next_page(self):
        pass
