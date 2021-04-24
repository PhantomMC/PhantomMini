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
        "configVersion" : 8,
        "serverInfo" : {
            "host" : "0.0.0.0",
            "port" : 25565
        },
        "Style" : 1, #chose between 1, 2 and 3
        "Content" : {
            "lowerMessage" : "A message",
            "upperMessage": "This msg appears above the server!",
            "hoverMessage" : "You should have brought a config",
            "kickMessage" : "Angry",
            "imagePath" : "server-icon.png"
        },
        "Logging" : 
            {
                "storeMessages" : False,
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
        print("config: ",self.config)
        #command_manager().start()
        
        self.logger = logger(Version,self.config)
        
        plugin_id = 10892
        bstats(plugin_id, self.logger).start()
        self.json_creator = json_creator(self.config,self.logger)
        self.host = self.config["serverInfo"]["host"]
        self.port = int(self.config["serverInfo"]["port"])
        
        self.logger.debug("hoverMessage:",self.config["Content"]["kickMessage"])
    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.debug("host:", self.host,"port",self.port)
        addr_info = socket.getaddrinfo(self.host,self.port)
        try:
            s.bind(addr_info[0][-1])
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
