import re
import math
import time

class Page(object):
    _instance = None

    def __new__(cls, *args):
        if not cls._instance:
            cls._instance = super(Page, cls).__new__(cls)
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
            if "/" in self.mcdu.scratch:
                value = tuple(self.mcdu.scratch.split('/'))
            else:
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
    gpstime = "^([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$"
    latitude = u"^[0-9]{2}\u00b0[0-9]{2}[.][0-9][NS]$"
    longitude =u"^(0[0-9]{2}|1[0-8][0-9])\u00b0[0-9]{2}[.][0-9][WE]$"
    coroute = "^GL[A-Z]{8}$"
    flightlevel = "^([0-3][0-9]{4})|(FL[1-3][0-9]{2})$"
    temperature = "^[+-][0-9]{2}$"
    heading = "^([0-2]{0:1}[0-9]{2})|(3[0-5][0-9])$"
    speedknots = "^{[0-9]{0:3}$"

    white = "#ffffff"
    blue = "#20c2e3"
    orange = "#ffaf47"
#    green = "#00ff00"
    green = "#8fac99"

    mandatory = 1
    optional = 0

    def convertToLatitudeString(self, lat):
        if (lat < 0):
            lat = -lat
            d = "S"
        else:
            d = "N"
        p1 = int(math.floor(lat))
        p2 = int(math.floor((lat-p1)*100))
        p3 = int(math.floor((((lat-p1)*100)-p2)*100))
        return u'{0:2d}\u00b0{1:2d}.{2:1d}{3:1s}'.format(p1, p2, p3, d)

    def convertToLongitudeString(self, lon):
        if lon < 0:
            d = "W"
            lon = -lon
        elif lon > 180.0:
            d = "W"
            lon = 360.0 - lon
        else:
            d = "E"
        p1 = int(math.floor(lon))
        p2 = int(math.floor((lon-p1)*100))
        p3 = int(math.floor((((lon-p1)*100)-p2)*100))
        return u'{0:3d}\u00b0{1:2d}.{2:1d}{3:1s}'.format(p1, p2, p3, d)

    def convertAltitudeToFlightLevel(self, value):
        if int(value) > 18000:
            return 'FL{0:3d}'.format(int(value/100))
        else:
            return value

    def convertToHeading(self, value):
        return u'{0:3d}\u00b0'.format(int(value))

    # Orange Rectangular fields for mandatory user entered data
    # Green dash fields for optional user entered data
    # Whether or not a field is mandatory or optional can be changed 
    def __init__(self, title, value, **kwargs):
        self.title = title
        self.format = kwargs.pop("format", None)
        self.action = kwargs.pop("action", None)
        self.update = kwargs.pop("update", None)
        self.color = kwargs.pop("color", Field.green)
        self.mode  = kwargs.pop("mode", Field.optional)
        self.cvtfunc = kwargs.pop("convert", None)

        if self.action:
            self.color = Field.blue

        if (type(value) == tuple):
            if self.mode == Field.optional:
                self.color = Field.green
                lst = list(value)
                for i in range(len(lst)):
                    if type(lst[i]) == int:
                        lst[i] = "-"*lst[i]
                self.value = tuple(lst)
            else:
                self.color = Field.orange
                lst = list(value)
                for i in range(len(lst)):
                    if type(lst[i]) == int:
                        lst[i] = u"\u25af"*lst[i]
                self.value = tuple(lst)

        elif (type(value) == int):
            if value < 0 or self.mode == Field.optional:
                self.color = Field.blue
                if value < 0:
                    value = -value
                self.value = "-"*value
            elif value > 0 or self.mode == Field.mandatory:
                self.color = Field.orange
                self.value = u"\u25af"*value
            else:
                self.value = ""
        elif (isinstance(value, time.struct_time)):
            self.color = Field.blue
            self.value = time.strftime("%H:%M:%S", value)
        else:
            self.value = value

    def validate(self, value):
        if type(value) == tuple:
            lst = list(value)
            fmt = list(self.format)
            for i in range(len(lst)):
                if fmt[i] and not re.match(fmt[i], lst[i]):
                    return ValueError
        else:
            try:
            	if self.format and not re.match(self.format, value):
                	raise ValueError
            except:
                print ("Fehler bei " + str(value), str(self.format))
                raise ValueError

    def dump(self):
        return {"title": self.title, "value": self.value, "color": self.color}

    def getValue(self):
        if type(self.value) == tuple:
            cvtfl = []
            fmts = list(self.format)
            if type(self.cvtfunc) == tuple:
                cvtfl = list(self.cvtfunc)
            lst = list(self.value)
            if not cvtfl or not cvtfl[0]:
                strg = lst[0]
            else:
                strg = cvtfl[0](self, lst[0])
            if fmts[0] == Field.temperature:
                strg += u"\u00b0"
            for i in range(1, len(lst)):
                if not cvtfl:
                    strg += "/" + lst[i]
                else:
                    strg += "/" + cvtfl[i](self,lst[i])
                if fmts[i] == Field.temperature:
                    strg += u"\u00b0"
            return strg
        else:
            return self.value
