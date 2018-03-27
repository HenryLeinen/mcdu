from mcdu.subsystem import Subsystem
from mcdu.page import Page, Field


class DATA(Subsystem):
	name = "DATA"

	def __init__(self, api):
		Subsystem.__init__(self)
		self.api = api

	def activate(self):
		self.mcdu.show(DataIndexPage)


class DataIndexPage(Page):
	title = "DATA INDEX"

	def init(self):
		self.field(0, "POSITION", "<MONITOR", action=self.position_monitor)
		self.field(1, "IRS", "<MONITOR", action=self.irs_monitor)
		self.field(2, "GPS", "<MONITOR", action=self.gps_monitor)
		self.field(3, "", "A/C STATUS", action=self.a_c_status)
		self.field(4, "", "")
		self.field(4, "PRINT", "FUNCTION>", action=self.prnt)
		self.field(5, "", "")
		self.field(5, "AOC", "FUNCTION>", action=self.aoc)

	def position_monitor(self):
		pass

	def irs_monitor(self):
		pass

	def gps_monitor(self):
		pass

	def a_c_status(self):
		pass

	def prnt(self):
		pass

	def aoc(self):
		pass
