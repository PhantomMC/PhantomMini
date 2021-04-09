"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
"""
import socket
from pha_connection import connection_manager
from pha_json import json_creator
from pha_logging import logger
from pha_command import command_manager
from pha_yaml import yaml_manager
from pha_bstats import bstats

Version = "0.7.0"
defaultConfig = {
        "configVersion" : 6,
        "serverInfo" : {
            "host" : "51.222.28.81",
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
        "Logging" : 
            {
                "log" : False,
                "storeUsers":True
             },
        "debug" : False
        }


class phantom:
    def __init__(self):
        config_path = "config"
        is_config = True
        
        config_retriever = yaml_manager(defaultConfig,config_path,is_config)
        self.config = config_retriever.get_yml()
        
        command_manager().start()
        
        self.is_micropython = config_retriever.is_micropython
        
        
        self.logger = logger(Version,self.config)
        
        plugin_id = 10892
        bstats(plugin_id, self.is_micropython,self.logger).start()
        self.json_creator = json_creator(self.config,self.logger)
        self.host = self.config["serverInfo"]["host"]
        self.port = self.config["serverInfo"]["port"]
        
    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((self.host, self.port))
            i = 1
            while True:
                s.listen(1)
                conn, addr = s.accept()
                conn_mngr = connection_manager(conn,self.json_creator,self.logger,i,addr)
                conn_mngr.start()
                i += 1
            print("This will never get triggered, but has to be here because of python")
        finally:
            s.close()
    
    

phantomServer = phantom()

try:
    phantomServer.start()
except KeyboardInterrupt:
    print("Stopped....")
