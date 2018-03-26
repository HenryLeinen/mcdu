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
KEY_DEL = 21
KEY_DIR = 100
KEY_PROG= 101
KEY_PERF= 102
KEY_INIT= 103
KEY_DATA= 104
KEY_F_PLN=110
KEY_RAD_NAV=111
KEY_FUEL_PRED=112
KEY_SEC_F_PLN=113
KEY_ATC_COMM=114
KEY_MENU= 115
KEY_AIRPORT=120
KEY_PAGE_UP=121
KEY_PAGE_DN=122
KEY_NEXT_PAGE=130
KEY_LSK1L = 1
KEY_LSK6L = 6
KEY_LSK1R = 11
KEY_LSK6R = 16
KEY_A = 65
KEY_Z = ord('Z')
KEY_0 = 48
KEY_9 = ord('9')

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
		print "Class myDisplay initialize"
		self.root = Tk()
		self.fnt_ttl = tkFont.Font(family='AirbusMCDUa', size=ttlsize)
		self.fnt_big = tkFont.Font(family='AirbusMCDUa', size=bigsize)
		self.fnt_sml = tkFont.Font(family='AirbusMCDUa', size=smlsize)


	# required method, called from main
	def initialize(self, mcdu):
		self.LOOP_ACTIVE = True
		print "Initializing"
		self.createWidgets()
		self.mcdu = mcdu

	# required method, called from main
	def open(self):
		self.mcdu.add_display(self)

	# unused method, not called hopefully --> instead everything done via messageloop
	def on_message(self, message):
		print "Unused method 'on_message' called"
		if message == "DEL":
			self.mcdu.scratch_delete()
		elif message == "CLR":
			self.mcdu.scratch_clear()
		elif message.startswith("LSK"):
			num = int(message[3])
			if message[4] == "L": side = 0
			else: side = 1
			self.mcdu.lsk((num,side))
		elif message == "MENU":
			self.mcdu.menu()
		else:
			self.mcdu.scratch_input(message)

	# required method
	def update_row(self, index):
		self.update()

	# required method
	def update_scratch(self):
		self.w.itemconfigure("SCRATCH", text=self.mcdu.scratch_text())

	# required method
	def on_close(self):
		self.mcdu.remove_display(self)
		self.root.destroy()
		self.LOOP_ACTIVE = False
		print "Exiting"

	def on_click(self, event):
		self.on_close()

	# required method
	def update(self):
		fields = self.mcdu.page.fields
		self.update_scratch()
		self.w.itemconfigure("TITLE",   text=self.mcdu.page.title)
		for i in range(0,6):
			field = fields[i]
			t = "LSK"+str(i)
			if field:
				self.w.itemconfigure(t+"L", text=field[0].title)
				self.w.itemconfigure(t+"Ls",text=field[0].value, fill=field[0].color)
				if len(field)>1:
					self.w.itemconfigure(t+"R", text=field[1].title)
					self.w.itemconfigure(t+"Rs",text=field[1].value, fill=field[1].color)
				else:
					self.w.itemconfigure(t+"R", text=" ")
					self.w.itemconfigure(t+"Rs",text=" ")
			else:
				self.w.itemconfigure(t+"L", text=" ")
				self.w.itemconfigure(t+"Ls",text=" ")
				self.w.itemconfigure(t+"R", text=" ")
				self.w.itemconfigure(t+"Rs",text=" ")

	def createWidgets(self):
		print "Creating widgets"
 		self.root.overrideredirect(True)
		self.root.wm_geometry("1024x768")
		self.root.bind("<Button-1>", self.on_click)
		self.w = Canvas(self.root, width=1024, height=768, bd=0, highlightthickness=0, bg='black', relief='ridge')
		self.w.pack()

		# Create the title
		self.w.create_text( colt, rowt, text=" ", font=self.fnt_big, fill="#ffffff", tags="TITLE", anchor=N)
		# Create the scratchpad
		self.w.create_text( coll, rowsc,text=" ", font=self.fnt_big, fill="#ffffff", tags="SCRATCH", anchor=NW)
		# Create the lines
		self.w.create_text( coll, row0, text=" ", font=self.fnt_sml, fill="#ffffff", tags="LSK0L", anchor=NW)
		self.w.create_text( coll, row0s,text=" ", font=self.fnt_big, fill="#ffffff", tags="LSK0Ls",anchor=NW)
		self.w.create_text( colr, row0, text=" ", font=self.fnt_sml, fill="#ffffff", tags="LSK0R", anchor=NE)
		self.w.create_text( colr, row0s,text=" ", font=self.fnt_big, fill="#ffffff", tags="LSK0Rs",anchor=NE)

		self.w.create_text( coll, row1, text=" ", font=self.fnt_sml, fill="#ffffff", tags="LSK1L", anchor=NW)
		self.w.create_text( coll, row1s,text=" ", font=self.fnt_big, fill="#ffffff", tags="LSK1Ls",anchor=NW)
		self.w.create_text( colr, row1, text=" ", font=self.fnt_sml, fill="#ffffff", tags="LSK1R", anchor=NE)
		self.w.create_text( colr, row1s,text=" ", font=self.fnt_big, fill="#ffffff", tags="LSK1Rs",anchor=NE)

		self.w.create_text( coll, row2, text=" ", font=self.fnt_sml, fill="#ffffff", tags="LSK2L", anchor=NW)
		self.w.create_text( coll, row2s,text=" ", font=self.fnt_big, fill="#ffffff", tags="LSK2Ls",anchor=NW)
		self.w.create_text( colr, row2, text=" ", font=self.fnt_sml, fill="#ffffff", tags="LSK2R", anchor=NE)
		self.w.create_text( colr, row2s,text=" ", font=self.fnt_big, fill="#ffffff", tags="LSK2Rs",anchor=NE)

		self.w.create_text( coll, row3, text=" ", font=self.fnt_sml, fill="#ffffff", tags="LSK3L", anchor=NW)
		self.w.create_text( coll, row3s,text=" ", font=self.fnt_big, fill="#ffffff", tags="LSK3Ls",anchor=NW)
		self.w.create_text( colr, row3, text=" ", font=self.fnt_sml, fill="#ffffff", tags="LSK3R", anchor=NE)
		self.w.create_text( colr, row3s,text=" ", font=self.fnt_big, fill="#ffffff", tags="LSK3Rs",anchor=NE)

		self.w.create_text( coll, row4, text=" ", font=self.fnt_sml, fill="#ffffff", tags="LSK4L", anchor=NW)
		self.w.create_text( coll, row4s,text=" ", font=self.fnt_big, fill="#ffffff", tags="LSK4Ls",anchor=NW)
		self.w.create_text( colr, row4, text=" ", font=self.fnt_sml, fill="#ffffff", tags="LSK4R", anchor=NE)
		self.w.create_text( colr, row4s,text=" ", font=self.fnt_big, fill="#ffffff", tags="LSK4Rs",anchor=NE)

		self.w.create_text( coll, row5, text=" ", font=self.fnt_sml, fill="#ffffff", tags="LSK5L", anchor=NW)
		self.w.create_text( coll, row5s,text=" ", font=self.fnt_big, fill="#ffffff", tags="LSK5Ls",anchor=NW)
		self.w.create_text( colr, row5, text=" ", font=self.fnt_sml, fill="#ffffff", tags="LSK5R", anchor=NE)
		self.w.create_text( colr, row5s,text=" ", font=self.fnt_big, fill="#ffffff", tags="LSK5Rs",anchor=NE)


	def parseInput(self, byte):
		print "Received byte "+ byte
		cmd = ord(byte)
		if cmd >= KEY_LSK1L and cmd <= KEY_LSK6L:
			num = cmd-1
			side = 0
			print "KEY: LSK"+str(num)+"L"
			self.mcdu.lsk((num,side))
		elif cmd >= KEY_LSK1R and cmd <= KEY_LSK6R:
			num = cmd - 11
			side = 1
			print "KEY: LSK"+str(num)+"R"
			self.mcdu.lsk((num,side))
		elif cmd == KEY_CLR:
			print "KEY: CLR"
			self.mcdu.scratch_clear()
		elif cmd == KEY_DEL:
			print "KEY: DEL"
			self.mcdu.scratch_delete()
		elif cmd == KEY_MENU:
			print "KEY: MENU"
			self.mcdu.menu()
		elif cmd == KEY_DIR:
			print "KEY: DIR"
			self.mcdu.dir()
		elif cmd == KEY_PROG:
			print "KEY: PROG"
			self.mcdu.prog()
		elif cmd == KEY_F_PLN:
			print "KEY: F-PLN"
			self.mcdu.f_pln()
		elif cmd == KEY_PERF:
			print "KEY: PERF"
			self.mcdu.perf()
		elif cmd == KEY_INIT:
			print "KEY: INIT"
			self.mcdu.init()
		elif cmd == KEY_DATA:
			print "KEY: DATA"
			self.mcdu.data()
		elif cmd >= KEY_A and cmd <= KEY_Z:
			self.mcdu.scratch_input(byte)
		elif cmd >= KEY_0 and cmd <= KEY_9:
			self.mcdu.scratch_input(byte)
		else:
			print "Byte received " + byte

	def mainloop(self):
		print "Entering Mainloop"
		self.LOOP_ACTIVE = True
		with open("/dev/kbdscan", "ro") as f:
			while self.LOOP_ACTIVE:
				self.root.update()
				byte = f.read(1)
				if byte != "":
					self.parseInput(byte)
		print "Leaving Mainloop"



# m = myDisplay()
# m.mainloop()
