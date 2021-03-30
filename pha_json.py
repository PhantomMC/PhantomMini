# -*- coding: utf-8 -*-
"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
"""
import re
import base64
import json
from pha_logging import info
class json_creator:
    
    def __init__(self,config):
        self.Content = config["Content"]
        self.Style = config["Style"]
        info("Loaded style",self.Style)
        self.load_base64()
        self.create_Response_dictionary()
        self.disconnect_dictionary = {"text":self.Content["kickMessage"]}
    def fix_coloring(self,text):
        #TODO add a \& option
        text = re.sub("&","§",text)
        return text
    def change_Response_dictionary(self,protocol_version):
        max_players = 0
        if self.Style == 3:
            max_players = 1
        if self.Style == 1:
            protocol_version = -1;
        
        self.response_dict["version"]["protocol"] = protocol_version
        self.response_dict["players"]["max"] = max_players
        
    def create_Response_dictionary(self):
        virtual_Playernames = re.split("\n", self.Content["hoverMessage"])
        
        virtual_players = []
        for playername in virtual_Playernames:
            playerDict = {"name":self.fix_coloring(playername),"id": "4566e69f-c907-48ee-8d71-d7ba5aa00d20"}
            virtual_players.append(playerDict)
        
        
        
        
        
        self.response_dict = {
            "version" : {
                "name":"§r" + self.fix_coloring(self.Content["upperMessage"]),
                "protocol" : -1
                },
            "players": {
                "max": 0,
                "online": 0,
                "sample" : virtual_players},
            "description": self.fix_coloring(self.Content["lowerMessage"]),
            "favicon": "data:image/png;base64" + self.base64_message
        }
        
    def get_disconnect_dictionary_string(self):
        return json.dumps(self.disconnect_dictionary)
        
    def load_base64(self):
        binary_file = open(self.Content["imagePath"],'rb')
        
        try:
            binary_file_data = binary_file.read()
            base64_encoded_data = base64.b64encode(binary_file_data)
            self.base64_message = base64_encoded_data.decode('utf-8')
        except UnicodeDecodeError:
            print("Can't find image from imagepath")
        finally:
            binary_file.close()
            
    
    def get_JSON_string(self):
        return json.dumps(self.response_dict)