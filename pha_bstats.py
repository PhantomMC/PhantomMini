# -*- coding: utf-8 -*-
"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.

@author: Thorin, Erèsue
"""

from random import uniform
from platform import system, architecture, release
from psutil import cpu_count

class bstats:
    def __init__(self,plugin_id,is_micropython):
        self.create_bstat_dictionary()
        self.id = plugin_id
        self.is_micropython = is_micropython
        self.uuid = self.generate_UUID()
        
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
    
    #main logic for sending data to bstats
    def run(self):
        initial_delay = 1000*60*3*(1+uniform(0, 1)) # why not replace random with 1/2 ?? that has the same average effect
        second_delay = 1000*60*30*(uniform(0, 1))
        
        #wait initial_delay
        
        #send data
        
        #run a loop that sends data with a delay of second_delay
        
    #metod used to innitiate sending data to bstats
    def start(self):
        #run async thread of run
        1
        
    def generate_UUID(self):
        """
        This is for serverUUID; it must be the same for every
        request sent from a specific instance. A request sent
        with a UUID that has already been used will be denied
        unless it is sent from the same instance
        """