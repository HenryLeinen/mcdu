import sys

'''
A Python class implementing KBHIT, the standard keyboard-interrupt poller.
Works transparently on Windows and Posix (Linux, Mac OS X).  Doesn't work
with IDLE.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''

import os

# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import sys
    import termios
    import atexit
    from select import select


class KBHit:

	def __init__(self):
		'''Creates a KBHit object that you can call to do various keyboard things.
		'''
		if os.name == 'nt':
			pass
		else:
			# Save the terminal settings
			self.fd = sys.stdin.fileno()
			self.new_term = termios.tcgetattr(self.fd)
			self.old_term = termios.tcgetattr(self.fd)

			# New terminal setting unbuffered
			self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
			termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

			# Support normal-terminal reset at exit
			atexit.register(self.set_normal_term)

	def set_normal_term(self):
		''' Resets to normal terminal.  On Windows this is a no-op.
		'''
		if os.name == 'nt':
			pass
		else:
			termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

	def getch(self):
		''' Returns a keyboard character after kbhit() has been called.
		Should not be called in the same program as getarrow().
		'''
#		s = ''
		if os.name == 'nt':
			c = msvcrt.getch()
			if ord(c) == 0xE0:
				c = msvcrt.getch()
				vals = [72,77,80,75]
				return chr(vals.index(ord(c.decode('utf-8'))))
			return c.decode('utf-8')
		else:
			return sys.stdin.read(1)

	def getarrow(self):
		''' Returns an arrow-key code after kbhit() has been called. Codes are
		0 : up
		1 : right
		2 : down
		3 : left
		Should not be called in the same program as getch().
		'''
		if os.name == 'nt':
			msvcrt.getch() # skip 0xE0
			c = msvcrt.getch()
			vals = [72, 77, 80, 75]
		else:
			c = sys.stdin.read(3)[2]
			vals = [65, 67, 66, 68]
		return vals.index(ord(c.decode('utf-8')))

	def kbhit(self):
		''' Returns True if keyboard character was hit, False otherwise.
		'''
		if os.name == 'nt':
			return msvcrt.kbhit()
		else:
			dr,_,_ = select([sys.stdin], [], [], 0)
			return dr != []





class keyboard:

	def interpret_char(self, char):
		cmd = ord(char)
		if cmd in self.keymap:
			message = self.keymap[cmd]
		else:
			message = char
		return message

	def open(self):
		self.noInput = False
		try:
			self.file = open("/dev/kbdscan","r")
		except:
			self.noInput = True					# No KbdScan device, so use the regular stdin keyboard
			self.kb = KBHit()
		try:
			from configparser import SafeConfigParser
		except ImportError:
			from ConfigParser import SafeConfigParser
		config = SafeConfigParser()
		config.read("config/defaults.cfg")
		config.read("~/.config/mcdu.cfg")
		config.read("config/mcdu.cfg")
		self.keymap = {}
		self.keymap[config.getint("KeyMap", "KEY_CLR")] = "CLR"
		self.keymap[config.getint("KeyMap", "KEY_DEL")] = "DEL"
		self.keymap[config.getint("KeyMap", "KEY_DIR")] = "DIR"
		self.keymap[config.getint("KeyMap", "KEY_PROG")] = "PROG"
		self.keymap[config.getint("KeyMap", "KEY_PERF")] = "PERF"
		self.keymap[config.getint("KeyMap", "KEY_INIT")] = "INIT"
		self.keymap[config.getint("KeyMap", "KEY_DATA")] = "DATA"
		self.keymap[config.getint("KeyMap", "KEY_F_PLN")] = "F_PLN"
		self.keymap[config.getint("KeyMap", "KEY_RAD_NAV")] = "RAD_NAV"
		self.keymap[config.getint("KeyMap", "KEY_FUEL_PRED")] = "FUEL_PRED"
		self.keymap[config.getint("KeyMap", "KEY_SEC_F_PLN")] = "SEC_F_PLN"
		self.keymap[config.getint("KeyMap", "KEY_ATC_COMM")] = "ATC_COMM"
		self.keymap[config.getint("KeyMap", "KEY_MENU")] = "MENU"
		self.keymap[config.getint("KeyMap", "KEY_DIM")] = "DIM"
		self.keymap[config.getint("KeyMap", "KEY_AIRPORT")] = "AIRPORT"
		self.keymap[config.getint("KeyMap", "KEY_PAGE_UP")] = "PAGE_UP"
		self.keymap[config.getint("KeyMap", "KEY_NEXT_PAGE")] = "NEXT_PAGE"
		self.keymap[config.getint("KeyMap", "KEY_PAGE_DN")] = "PAGE_DN"
		self.keymap[config.getint("KeyMap", "KEY_LSK1L"  )] = "LSK0L"
		self.keymap[config.getint("KeyMap", "KEY_LSK2L"  )] = "LSK1L"
		self.keymap[config.getint("KeyMap", "KEY_LSK3L"  )] = "LSK2L"
		self.keymap[config.getint("KeyMap", "KEY_LSK4L"  )] = "LSK3L"
		self.keymap[config.getint("KeyMap", "KEY_LSK5L"  )] = "LSK4L"
		self.keymap[config.getint("KeyMap", "KEY_LSK6L"  )] = "LSK5L"
		self.keymap[config.getint("KeyMap", "KEY_LSK1R"  )] = "LSK0R"
		self.keymap[config.getint("KeyMap", "KEY_LSK2R"  )] = "LSK1R"
		self.keymap[config.getint("KeyMap", "KEY_LSK3R"  )] = "LSK2R"
		self.keymap[config.getint("KeyMap", "KEY_LSK4R"  )] = "LSK3R"
		self.keymap[config.getint("KeyMap", "KEY_LSK5R"  )] = "LSK4R"
		self.keymap[config.getint("KeyMap", "KEY_LSK6R"  )] = "LSK5R"


	def close(self):
		if self.noInput:
			pass
		else:
			self.file.close()

	def read(self):
		message = ""
		if not self.noInput:
			byte = self.file.read(1)
			if byte != "":
				print ("Received char "+byte+" KeyCode:" + str(ord(byte)))
				message = self.interpret_char(byte)
				if not message:
					message=byte
				print ("Maps to message "+message)
			else:
				message = ""
		else:
			if self.kb.kbhit():
				byte = self.kb.getch()
				print ("Received char " , byte , " KeyCode." + str(ord(byte)))
				if byte == '!':	# '!' activates the INIT page
					message = "INIT"
				elif byte == '\"':			# '"' activates the DATA page
					message = "DATA"
				elif byte == '$':			# activates the F_PLN page
					message = "F_PLN"
				elif byte == '%':			# activates the PERF page
					message ="PERF"
				elif ord(byte) == 0:		# arrow up
					message = "PAGE_UP"
				elif ord(byte) == 2:		# arrow dn
					message = "PAGE_DN"
				elif ord(byte) == 1:		# arrow right
					message = "NEXT_PAG"
				elif ord(byte) == 3:		# arrow left
					message = "AIRPORT"
				elif ord(byte) == 8:		# DEL key
					message = "CLR"
				else:
					message = self.interpret_char(byte)
				if not message:
					message=byte
				print ("Maps to message "+message)
			else:
				message = ""
		return message


