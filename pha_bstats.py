# -*- coding: utf-8 -*-
"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.

@author: Thorin, Erèsue
"""

import random
from platform import system, architecture, release
from psutil import cpu_count
import threading
import time
import requests
import uuid
import json

class bstats(threading.Thread):
    def __init__(self,plugin_id,is_micropython):
        threading.Thread.__init__(self)
        self.id = plugin_id
        self.create_bstat_dictionary()
        self.is_micropython = is_micropython
        
    def create_bstat_dictionary(self):
        arch = architecture()
        serverUUID = uuid.uuid1()
        self.bstat_dict = {
          "serverUUID": serverUUID.__str__(),
          "osName": system(),
          "osArch": arch[1] +" " + arch[0],
          "osVersion": release(),
          "coreCount": cpu_count(),
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
    def send_data(self):
        
        url = 'https://bstats.org/submitData/server-implementation'
        json_msg = json.dumps(self.bstat_dict)
        print(json_msg)
        res = requests.post(url, json=json_msg)
        print(res.text)
        
    
    def run(self):
        initial_delay = 60*3*(1+random.uniform(0, 1))#seconds
        second_delay = 60*30*(random.uniform(0, 1)) 
        loop_delay = 60*30
        
        time.sleep(initial_delay)
        self.send_data()
        
        time.sleep(second_delay+initial_delay)
        while True:
            self.send_data()
            time.sleep(loop_delay)