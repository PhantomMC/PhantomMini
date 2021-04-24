# -*- coding: utf-8 -*-
"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
@author: Thorin, Erèsue
"""
import ujson
import os
import threading
import time
import urequests as requests
import uuid
import ubinascii

def randrange(start, stop=None):
    if stop is None:
        stop = start
        start = 0
    upper = stop - start
    bits = 0
    pwr2 = 1
    while upper > pwr2:
        pwr2 <<= 1
        bits += 1
    if bits == 0:
        return start
    while True:
        r = getrandbits(bits)
        if r < upper:
            break
    return r + start
#generate a random real number between 0 and 1
def random_double():
    return randrange(0,1)

class bstats(threading.Thread):
    def __init__(self,plugin_id,logger):
        threading.Thread.__init__(self)
        self.id = plugin_id
        self.create_bstat_dictionary()
        self.logger = logger
        
    def create_bstat_dictionary(self):
        #systeminfo = os.uname()
        systeminfo = ["you", " are", " ", 1 , 4]
        sysname = systeminfo[0]
        release = systeminfo[2]
        version = systeminfo[3]
        machine = systeminfo[4]
        serverUUID = self.generate_uuid()
        self.bstat_dict = {
          "serverUUID": serverUUID.__str__(),
          "osName": sysname,
          "osArch": "Empty for now",
          "osVersion": version,
          "coreCount": machine,
          "plugins": [
            {
              "pluginName": "Phantom",
              "id": self.id,
              "pluginVersion": 0,
              "customCharts": [
                {
                  "chartId": "pings",
                  "data": [
                    {
                      "value": 6
                    }
                  ]
                },
                {
                  "chartId": "joins",
                  "data": [
                    {
                      "value": 3
                    }
                  ]
                },
                {
                  "chartId": "logging",
                  "data": [
                    {
                      "value": "all"
                    }
                  ]
                },
                {
                  "chartId": "mode",
                  "data": [
                    {
                      "value": "2"
                    }
                  ]
                }
              ]
            }
          ]
        }
        self.bstats_json = ujson.dumps(self.bstat_dict)
    def send_data(self):
        
        url = 'https://bstats.org/submitData/server-implementation'
        res = requests.post(url,data = self.bstat_dict)
        self.logger.debug("Sent message to bstats")
        if res.text == "":
            pass #TODO idk, some errorprocessing
        
    
    def run(self):
        initial_delay = 60*3*(1+random_double())#seconds
        second_delay = 60*30*(random_double()) 
        loop_delay = 60*30
        
        time.sleep(initial_delay)
        self.send_data()
        
        time.sleep(second_delay+initial_delay)
        while True:
            self.send_data()
            time.sleep(loop_delay)
    def generate_uuid(self):
        """Generates a random UUID compliant to RFC 4122 pg.14"""
        random = bytearray(os.urandom(16))
        random[6] = (random[6] & 0x0F) | 0x40
        random[8] = (random[8] & 0x3F) | 0x80
        return UUID(bytes=random)
        
class UUID:
    def __init__(self, bytes):
        if len(bytes) != 16:
            raise ValueError('bytes arg must be 16 bytes long')
        self._bytes = bytes

    @property
    def hex(self):
        return ubinascii.hexlify(self._bytes).decode()

    def __str__(self):
        h = self.hex
        return '-'.join((h[0:8], h[8:12], h[12:16], h[16:20], h[20:32]))

    def __repr__(self):
        return "<UUID: %s>" % str(self)

