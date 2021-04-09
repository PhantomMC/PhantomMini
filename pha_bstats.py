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
class bstats(threading.Thread):
    def __init__(self,plugin_id,is_micropython):
        threading.Thread.__init__(self)
        self.uuid = self.generate_UUID()
        self.id = plugin_id
        self.create_bstat_dictionary()
        self.is_micropython = is_micropython
        
    def create_bstat_dictionary(self):
        self.bstat_dict = {
          "serverUUID": self.server_UUID,
          "osName": system(),
          "osArch": architecture(),
          "osVersion": release(),
          "coreCount": cpu_count(),
          "plugins": [
            {
              "pluginName": "Phantom",
              "id": self.id,
              "pluginVersion": 0,
              "customCharts": []
            }
          ]
        }
    def send_data(self):
        #send data to https://bstats.org/submitData/server-implementation
        url = 'https://bstats.org/submitData/server-implementation'
        res = requests.post(url, data=self.bstat_dict)
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
    def generate_UUID(self):
        """
        This is for serverUUID; it must be the same for every
        request sent from a specific instance. A request sent
        with a UUID that has already been used will be denied
        unless it is sent from the same instance
        """
        self.server_UUID = "23b49a13-cc32-4d45-a9ce-e7e896c2ff43"