import sys

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
			self.file = open("/dev/kbdscan","ro")
		except:
			self.noInput = True
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
#		self.file.close()
		pass

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
		return message


