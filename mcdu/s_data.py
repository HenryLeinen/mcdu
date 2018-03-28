from subsystem import Subsystem
from page import Page, Field


class DATA(Subsystem):
	name = "DATA"

	def __init__(self, api):
		Subsystem.__init__(self)
		self.api = api

	def activate(self):
		self.mcdu.show(DataIndexPage1)
		self.activePage = 1

	def next_page(self):
		if self.activePage == 2:
			self.mcdu.show(DataIndexPage1)
			self.activePage = 1
		else:
			self.mcdu.show(DataIndexPage2)
			self.activePage = 2

class DataIndexPage1(Page):
	title = "DATA INDEX     1/2"

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


class DataIndexPage2(Page):
	title = "DATA INDEX     2/2"

	def init(self):
		self.field(0, "", "<WAYPOINTS", action=self.waypoints)
		self.field(0, "PILOTS", "WAYPOINTS>", action=self.pilotWaypoints)
		self.field(1, "", "<NAVAIDS", action=self.navaids)
		self.field(1, "PILOTS", "NAVAIDS>", action=self.pilotNavaids)
		self.field(2, "", "<RUNWAYS", action=self.runways)
		self.field(2, "PILOTS", "RUNWAYS>", action=self.pilotRunways)
		self.field(3, "", "<ROUTES", action=self.routes)
		self.field(3, "PILOTS", "ROUTES>", action=self.pilotRoutes)
		self.field(4, "ACTIVE F-PLN", "<WINDS", action=self.winds)
		self.field(5, "SEC F-PLN", "<WINDS", action=self.secWinds)

	def waypoints(self):
		pass
	
	def pilotWaypoints(self):
		pass

	def navaids(self):
		pass

	def pilotNavaids(self):
		pass

	def runways(self):
		pass

	def pilotRunways(self):
		pass

	def routes(self):
		pass

	def pilotRoutes(self):
		pass

	def winds(self):
		pass

	def secWinds(self):
		pass

class A_C_StatusPage(Page):
	title = "Checking..."
	engine = "Checking.."

	def init(self):
		self.engine = ""
		self.title = "Checking"

	def refresh(self):
		self.clear()

		if self.engine:
			self.page(1, "    ENG", self.engine)

		Page.refresh(self)