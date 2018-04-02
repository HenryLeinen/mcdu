from mcdu.avionics import Avionics

import threading
import socket
import struct
import binascii

class XPlaneReceiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(3.0)

        self.avionics = Avionics()
        self.active = True

        self.datarefs = {}      # key = index, value = dataref
        self.datarefidx = 0     # first index is 0

        self.UDP_PORT = 49000
#        self.UDP_ADDR = "192.168.178.87"
        self.UDP_ADDR = "127.0.0.1"

        self.xplaneValues = {}

    def request(self, dataref, freq= None):
        # check if frequency is default (not provided)
        if freq == None:
            freq = 1        # default frequency is 1 message per second

        # check whether dataref is already requested
        if dataref in self.datarefs.values():
            # get the index
            idx = list(self.datarefs.keys()) [list(self.datarefs.values()).index(dataref)]
            # check if we want to stop receiving the dataref
            if freq == 0:
                # check if dataref also exists in the xplaneValues
                if dataref in self.xplaneValues.keys():
                    del self.xplaneValues[dataref]
                del self.datarefs[idx]
        else:
            idx = self.datarefidx
            self.datarefs[self.datarefidx] = dataref
            self.datarefidx += 1
        cmd = b"RREF\x00"
        string = dataref.encode()
        message = struct.pack("<5sii400s", cmd, freq, idx, string)
        print ("Requesting " + dataref + " with index " + str(idx))
        assert(len(message)==413)
        self.sock.sendto(message, (self.UDP_ADDR, self.UDP_PORT))

    def do_request(self):
        self.request("sim/flightmodel/position/groundspeed")         # as float in m/s
        self.request("sim/flightmodel/position/indicated_airspeed")  # as float in kias
        self.request("sim/flightmodel/position/true_airspeed")       # as float in m/s

        self.request("sim/flightmodel/position/latitude",2)            # as double in degrees
        self.request("sim/flightmodel/position/longitude")           # as double in degrees
        self.request("sim/flightmodel/position/elevation")           # as double in meters

        self.request("sim/cockpit/gps/course")                       # 

        self.request("sim/time/local_time_sec")                      # local time as seconds since midnight

    def parse(self, retvalues):
        update = {}

        print (self.xplaneValues)

        if "sim/flightmodel/position/groundspeed" in self.xplaneValues.keys():
            update["speed"] = self.xplaneValues["sim/flightmodel/position/groundspeed"]
            print ("update speed : ", update["speed"])
        if ("sim/flightmodel/position/latitude" in self.xplaneValues.keys()) and ("sim/flightmodel/position/longitude" in self.xplaneValues.keys()):
            update["pos"] = (self.xplaneValues["sim/flightmodel/position/latitude"], self.xplaneValues["sim/flightmodel/position/longitude"])
            print ("update position : ", update["pos"])

#        print (udpate["pos"])

#        for i in range(0, len(data), 36):
#            packet = struct.unpack("i8f", data[i:i+36])
#
#            if packet[0] == 3:
#                update["speed"] = int(round(packet[4]))
#            elif packet[0] == 5:
#                wind_heading = int(round(packet[5]))
#                wind_speed = int(round(packet[4]))
#                update["wind"] = "%i/%i" % (wind_heading, wind_speed)
#            elif packet[0] == 6:
#                update["temp"] = int(round(packet[2]))
#            elif packet[0] == 14:
#                update["gear"] = True if packet[1] > 0.1 else False
#                update["brk"] = True if packet[2] > 0.1 else False
#            elif packet[0] == 17:
#                update["hdg"] = int(round(packet[3]))
#            elif packet[0] == 20:
#                update["pos"] = (round(packet[1], 8), round(packet[2], 8))
#                update["alt"] = int(round(packet[3]))
#            elif packet[0] == 37:
#                update["eng"] = (packet[1], packet[2], packet[3], packet[4])

        self.avionics.update(update)

    def run(self):
        self.sock.bind((self.UDP_ADDR, 49000))
        self.do_request()
        while self.active:
            try:
                # receive packet
                data, addr = self.sock.recvfrom(1024)
#                print ("Received ", binascii.hexlify(data))
                # decode packet
                retvalues = {}
                # read the header RREF
                header = data[0:5]
                if header != b"RREF\x00":
                    print ("Unknown packet received !", binascii.hexlify(data))
#                else:
                    # we get 8 bytes for each dataref sent:
                    # an integer for the idx and the float value
#                    values = data[5:12]
 #                   (freq, idx) = struct.unpack("<ii")
 #                   values = data[13:]
#                    if #### IMPLEMENT THE PARSING OF DATA AT THIS TIME ALREADY 
                        #

                    
#                    lenvalue = 8
#                    numvalues = int(len(values)/lenvalue)
#                    for i in range(0, numvalues):
#                        singledata=data[(9+lenvalue*i):(9+lenvalue*(i+1))]
#                        (idx, value) = struct.unpack("<if", singledata)
#                        if (idx == 3):
#                            print ("GPS: ", binascii.hexlify(data))
#                        if idx in self.datarefs.keys():
#                            # convert negativ 0.0 values to positive 0.0
#                            if value < 0.0 and value > -0.001 :
#                                value = 0.0
#                            retvalues[self.datarefs[idx]] = value
#
#                self.xplaneValues.update(retvalues)
#                self.parse(retvalues)
            except socket.timeout:
                print ("Timeout on XPlaneReceiver")
#                self.do_request()
                pass
            except:
                print ("Bullshit exception")
        self.sock.close()
        

    def stop(self):
        self.active = False

