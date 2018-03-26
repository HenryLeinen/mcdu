import re

class Page(object):
    _instance = None

    def __new__(cls, *args):
        if not cls._instance:
            cls._instance = super(Page, cls).__new__(cls, *args)
            cls._instance.fields = None

        return cls._instance

    def __init__(self, mcdu, sys):
        self.mcdu = mcdu
        self.sys = sys

        if not self.fields:
            self.clear()
            init = getattr(self, "init", None)
            if init: init()

    def clear(self):
        self.fields = [[] for i in range(6)]

    def refresh(self):
        if self.mcdu.page == self:
            self.mcdu.update()

    def field(self, index, title, value, **kwargs):
        field = Field(title, value, **kwargs)

        if not self.fields[index]:
            self.fields[index] = [field]
        else:
            self.fields[index].append(field)

    def field_update(self, index, col, value):
        field = self.fields[index][col]
        field.value = value
        self.mcdu.update_row(index)

    def lsk(self, pos):
        num, side = pos

        fields = self.fields[num]

        # get the selected field
        if not fields:
            return
        elif side == 1 and len(fields) < 2:
            return
        elif side == 0:
            field = fields[0]
        elif side == 1:
            field = fields[-1]
        else:
            return

        if field.action:
            field.action()
            return

        # if the scratchpad is not empty, try to insert
        # the value into the selected row, otherwise copy
        # the selected row into the scratchpad
        if self.mcdu.scratch:
            if not field.update: return
            value = self.mcdu.scratch
            try:
                field.validate(value)
                field.update(value)
            except ValueError:
                self.mcdu.scratch_set("INVALID FORMAT")
            else:
                self.field_update(num, side, value)
                self.mcdu.scratch_clear()
        else:
            self.mcdu.scratch_set(field.value)

class Field(object):
    flightno = "^[A-Z]{3}[0-9A-Z]{1,4}$"
    time = "^([01][0-9]|2[0-3])[0-5][0-9]Z$"
    icao = "^[A-Z]{4}$"

    white = "#ffffff"
    blue = "#20c2e3"
    orange = "#ffaf47"

    def __init__(self, title, value, **kwargs):
        self.title = title
        self.format = kwargs.pop("format", None)
        self.action = kwargs.pop("action", None)
        self.update = kwargs.pop("update", None)
        self.color = kwargs.pop("color", Field.white)

        if self.action:
            self.color = Field.blue

        if (type(value) == int):
            if value < 0:
                self.color = Field.blue
                self.value = u"\u23b5"*(-value)
            elif value > 0:
                self.color = Field.orange
                self.value = u"\u25af"*value
            else:
                self.value = ""
        else:
            self.value = value

    def validate(self, value):
        if self.format and not re.match(self.format, value):
            raise ValueError

    def dump(self):
        return {"title": self.title, "value": self.value, "color": self.color}
