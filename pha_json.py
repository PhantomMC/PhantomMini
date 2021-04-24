# -*- coding: utf-8 -*-
"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
"""
import re
import base64
import ujson as json
class json_creator:
    
    def __init__(self,config,logger):
        self.logger = logger
        self.Content = config["Content"]
        self.Style = int(config["Style"])
        self.load_base64()
        self.UUIDlist = [
            "d2b440c3-edde-4443-899e-6825c31d0919",
            "b2957bef-7e6e-4872-b01e-6873034a535a"
            ]
        self.create_Response_dictionary()
        self.disconnect_dictionary = {"text":self.Content["kickMessage"]}
    def fix_text(self,text):
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
    
    @staticmethod
    def simple_split(astring, target_char):
        endlist = []
        startpos = 0
        for i in range(len(astring)):
            if(astring[i] == target_char):
                endlist.append(astring[startpos:i])
                startpos = i + 1
        endlist.append(astring[startpos:])
        return endlist
    
    def create_Response_dictionary(self):
        Playernames_str = self.Content["hoverMessage"]
        Playernames_str = self.fix_text(Playernames_str)
        virtual_Playernames = self.simple_split(Playernames_str, "\n")
        virtual_players = []
        index = 0
        for playername in virtual_Playernames:
            if index >= len(self.UUIDlist):
                index = 0
                
            playerDict = {"name":playername,"id": self.UUIDlist[index]}
            virtual_players.append(playerDict)
            index += 1
        
        
        
        
        
        self.response_dict = {
            "version" : {
                "name":"§r" + self.fix_text(self.Content["upperMessage"]),
                "protocol" : -1
                },
            "players": {
                "max": 0,
                "online": 0,
                "sample" : virtual_players},
            "description": self.fix_text(self.Content["lowerMessage"]),
            "favicon": "data:image/png;base64," + self.base64_message
        }
        
    
    def get_disconnect_dictionary_string(self):
        return json.dumps(self.disconnect_dictionary)
        
    def load_base64(self):
        filepath = self.Content["imagePath"]
        print(filepath)
        binary_file = open(filepath,'rb')
        
        try:
            binary_file_data = binary_file.read()
            base64_encoded_data = base64.b64encode(binary_file_data)
            self.base64_message = base64_encoded_data.decode('utf-8')
        except UnicodeDecodeError:
            print("Can't find image from imagepath")
        finally:
            binary_file.close()
            
    
    
    def get_JSON_string(self):
        msg = json.dumps(self.response_dict)
        self.logger.debug("json_message:",msg)
        self.logger.debug("saved_dictionary",self.response_dict)
        return msg