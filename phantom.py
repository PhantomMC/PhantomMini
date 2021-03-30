"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
"""
import socket
import yaml
import os
from connection_manager import connection_manager
from json_creator import json_creator
from pha_logging import send_message,logger,debug
from os import path



Version = "0.5.3"

defaultConfig = {
        "configVersion" : 4,
        "serverInfo" : {
            "host" : "localhost",
            "port" : 25565
        },
        "Style" : 1, #chose between 1, 2 and 3
        "Content" : {
            "lowerMessage" : "A message",
            "upperMessage": "This msg appears above the server!",
            "hoverMessage" : "You should have brought a config",
            "kickMessage" : "Angry",
            "imagePath" : "Logo.png"
        },
        "Logging" : {
            "pings" : { "log" : False },
            "connections" : {
                "list" : True,
                "log" : False
                }
            }
        }


class phantom:
    def __init__(self):
        self.logger = logger(Version)
        while not self.get_config():
            continue
        self.json_creator = json_creator(self.config)
        self.host = self.config["serverInfo"]["host"]
        self.port = self.config["serverInfo"]["port"]
    """
    @return True if successfull, False otherwise
    """
    
    
    
    def get_config(self):
        if path.exists("config.yml"):
            return self.load_config()
        else:
            send_message("No config was found, provididing a shittier one")
            self.write_config()
            return False
            
    def load_config(self):
        try:
            config_file = open("config.yml",encoding='utf8')
            self.config = yaml.safe_load(config_file)
            config_file.close()
            if(self.config["configVersion"] != defaultConfig["configVersion"]):
                return self.rename_config()
            return True
        except:
            config_file.close()
        return False
            
    def rename_config(self):
        send_message("Providing you with a newer config")
        if path.exists("config.old"):
            os.remove("config.old")
        os.rename("config.yml", "config.old")
        return self.write_config()
            
    def write_config(self):
        try:
            config_file = open("config.yml","w+")
            config_file.write(yaml.dump(defaultConfig))
        except:
            config_file.close()
            return False
        finally:
            config_file.close()
        return True
    
    def connection_actions(self,conn):
        try:
            conn_mngr = connection_manager(conn,self.json_creator)
            conn_mngr.do_response()
        finally:
            conn.close()
    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((self.host, self.port))
            while True:
                s.listen(1)
                conn, addr = s.accept()
                self.connection_actions(conn)
                debug("Closing connection...")
        finally:
            s.close()
    
    
    
    


phantomServer = phantom()

try:
    phantomServer.start()
except KeyboardInterrupt:
    1
