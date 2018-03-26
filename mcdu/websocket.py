import tornado.websocket
from tornado.escape import xhtml_escape
import json

class WebSocket(tornado.websocket.WebSocketHandler):
    def initialize(self, mcdu):
        self.mcdu = mcdu

    def open(self):
        self.mcdu.add_display(self)

    def on_message(self, message):
        if message == "DEL":
            self.mcdu.scratch_delete()
        elif message == "CLR":
            self.mcdu.scratch_clear()
        elif message.startswith("LSK"):
            num = int(message[3])
            if message[4] == "L": side = 0
            else: side = 1
            self.mcdu.lsk((num, side))
        elif message == "MENU":
            self.mcdu.menu()
        else:
            self.mcdu.scratch_input(message)

    def update_row(self, index):
        self.update()

    def update_scratch(self):
        data = json.dumps({
            "scratch": self.mcdu.scratch_text(),
        })
        self.write_message(data)

    def update(self):
        fields = self.mcdu.page.fields
        fields = [[field.dump() for field in row] for row in fields]

        data = json.dumps({
            "title": self.mcdu.page.title,
            "scratch": self.mcdu.scratch_text(),
            "fields": fields,
        })

        self.write_message(data);

    def on_close(self):
        self.mcdu.remove_display(self)
