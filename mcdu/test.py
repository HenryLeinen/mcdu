#!/usr/bin/env python
from Tkinter import *
import tkFont
import time

ttlsize = 30
bigsize = 38
smlsize = 20
half_spacing = smlsize+5
full_spacing = 112

KEY_CLR = 20

rowt = 5
row0 = rowt + bigsize
row0s = row0+half_spacing
row1 = row0+full_spacing
row1s = row1+half_spacing
row2 = row1+full_spacing
row2s = row2+half_spacing
row3 = row2+full_spacing
row3s = row3+half_spacing
row4 = row3+full_spacing
row4s = row4+half_spacing
row5 = row4+full_spacing
row5s = row5+half_spacing
rowsc = row5+full_spacing

coll = 20
colr = 1023-20
colt = 511


VAL_HDG = -1

class myDisplay(object):

	def __init__(self):

		self.blue= "#20c2e3"
		self.orange= "#ffaf47"
		self.white = "#ffffff"

		self.root = Tk() #roottk
		self.fnt_ttl = tkFont.Font(family='AirbusMCDUa', size=ttlsize)
		self.fnt_big = tkFont.Font(family='AirbusMCDUa', size=bigsize)
		self.fnt_sml = tkFont.Font(family='AirbusMCDUa', size=smlsize)

		self.title = " "
		self.scratch = " "
		self.rows = { 	"L0"	:	{ "static": {"column": coll, "row":row0, "anchor": NW},
						  "data"  : {"text": " ", "value": VAL_HDG, "heading": " "}},
				"L1"	:	{ "static": {"column": coll, "row":row1, "anchor": NW},
						  "data"  : {"text": " ", "value": VAL_HDG, "heading": " "}},
				"L2"	:	{ "static": {"column": coll, "row":row2, "anchor": NW},
						  "data"  : {"text": " ", "value": VAL_HDG, "heading": " "}},
				"L3"	:	{ "static": {"column": coll, "row":row3, "anchor": NW},
						  "data"  : {"text": " ", "value": VAL_HDG, "heading": " "}},
				"L4"	:	{ "static": {"column": coll, "row":row4, "anchor": NW},
						  "data"  : {"text": " ", "value": VAL_HDG, "heading": " "}},
				"L5"	:	{ "static": {"column": coll, "row":row5, "anchor": NW},
						  "data"  : {"text": " ", "value": VAL_HDG, "heading": " "}},
				"R0"	:	{ "static": {"column": colr, "row":row0, "anchor": NE},
						  "data"  : {"text": " ", "value": VAL_HDG, "heading": " "}},
				"R1"	:	{ "static": {"column": colr, "row":row1, "anchor": NE},
						  "data"  : {"text": " ", "value": VAL_HDG, "heading": " "}},
				"R2"	:	{ "static": {"column": colr, "row":row2, "anchor": NE},
						  "data"  : {"text": " ", "value": VAL_HDG, "heading": " "}},
				"R3"	:	{ "static": {"column": colr, "row":row3, "anchor": NE},
						  "data"  : {"text": " ", "value": VAL_HDG, "heading": " "}},
				"R4"	:	{ "static": {"column": colr, "row":row4, "anchor": NE},
						  "data"  : {"text": " ", "value": VAL_HDG, "heading": " "}},
				"R5"	:	{ "static": {"column": colr, "row":row5, "anchor": NE},
						  "data"  : {"text": " ", "value": VAL_HDG, "heading": " "}}
		}
		self.LOOP_ACTIVE = True
		print "Initializing"

	def exitProg(self, event):
		self.root.destroy()
		self.LOOP_ACTIVE = False
		print "Exiting"

	def updateRow(self,tag):
		if self.rows[tag]["data"]["value"] == VAL_HDG:
			clr = self.white
		elif self.rows[tag]["data"]["value"] == 0:
			clr = self.orange
		else:
			clr = self.blue
		self.w.itemconfigure(tag+"s", text=self.rows[tag]["data"]["heading"])
		self.w.itemconfigure(tag, text=self.rows[tag]["data"]["text"], fill=clr)

	def updateScratch(self):
		self.w.itemconfigure("SCRATCH", text=self.scratch)

	def updateAll(self):
		self.updateScratch()
		self.w.itemconfigure("TITLE",   text=self.title)
		for tag in self.rows.keys():
			self.updateRow(tag)

	def createWidgets(self):

 		self.root.overrideredirect(True)
		self.root.wm_geometry("1024x768")
		self.root.bind("<Button-1>", self.exitProg)
		self.w = Canvas(self.root, width=1024, height=768, bd=0, highlightthickness=0, bg='black', relief='ridge')
		self.w.pack()

		# Create the title
		self.w.create_text( colt, rowt, text=self.title, font=self.fnt_big, fill=self.white, tags="TITLE", anchor=N)
		# Create the scratchpad
		self.w.create_text( coll, rowsc,text=self.scratch, font=self.fnt_big, fill=self.white, tags="SCRATCH", anchor=NW)
		# Create the lines
		for tag, data in self.rows.items():
			# Create the heading
			self.w.create_text( data["static"]["column"], data["static"]["row"], text=data["data"]["heading"], font=self.fnt_sml, fill=self.white, tags=tag+"s", anchor=data["static"]["anchor"])
			# Create the item
			self.w.create_text( data["static"]["column"], data["static"]["row"]+half_spacing, text=data["data"]["text"], font=self.fnt_big, fill=self.white, tags=tag, anchor=data["static"]["anchor"])

	def parseInput(self, byte):
		if byte >= 'A' and byte <= 'Z':
			self.scratch = self.scratch + byte
			self.updateScratch()
		elif byte >= '0' and byte <= '9':
			self.scratch = self.scratch + byte
			self.updateScratch()
		elif byte == KEY_CLR:
			self.scratch = ""
			self.updateScratch()
		else:
			print "Byte received ", ord(byte)

	def mainloop(self):
		self.title = "ACARS PREFLIGHT"
		self.rows["L0"]["data"] = { "heading": "SYSTEM INIT", "text": "<ARM", "value": -2}
		self.rows["L1"]["data"] = { "heading": "ORIGIN", "text": u"\u25af"*4, "value": 0}
		self.rows["L2"]["data"] = { "heading": "DEST", "text": u"\u25af"*4, "value": 0}
		self.rows["L3"]["data"] = { "heading": "ALTRNT", "text": u"\u23b5"*5, "value": 0}
		self.rows["L4"]["data"] = { "heading": "RECEIVED", "text": "<MESSAGES", "value": -2}
		self.rows["L5"]["data"] = { "heading": "ACARS", "text": "<INDEX", "value": -2}

		self.rows["R0"]["data"] = { "heading": "FLT NO", "text": u"\u25af"*7, "value": 0}
		self.rows["R1"]["data"] = { "heading": "PLAN DEP", "text": u"\u25af"*5, "value": 0}
		self.rows["R2"]["data"] = { "heading": "ETA", "text": u"\u25af"*5, "value": 0}
		self.rows["R3"]["data"] = { "heading": "COMPANY", "text": u"\u25af"*3, "value": 0}
		self.rows["R4"]["data"] = { "heading": " ", "text": "REQUESTS>", "value": -2}
		self.rows["R5"]["data"] = { "heading": " ", "text": "INFLIGHT>", "value": -2}
		self.updateAll()

		print "Entering Mainloop"
		self.LOOP_ACTIVE = True
		with open("/dev/kbdscan", "ro") as f:
			while self.LOOP_ACTIVE:
				self.root.update()
				byte = f.read(1)
				if byte != "":
					self.parseInput(byte)
		print "Leaving Mainloop"



m = myDisplay()
m.createWidgets()
m.updateAll()
# createWidgets()
# root.mainloop()
m.mainloop()
