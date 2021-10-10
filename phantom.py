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
from pha_yaml import yaml_manager
from pha_bstats import bstats
import threading

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


class server(threading.Thread):
    def __init__(self, config):
        self.logger = logger(Version,self.config)
        
        self.json_creator = json_creator(self.config,self.logger)
        self.host = self.config["serverInfo"]["host"]
        self.port = self.config["serverInfo"]["port"]
        
    def run(self):
        self.listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.listeningSocket.bind((self.host, self.port))
            i = 1
            while True:
                self.listeningSocket.listen(1)
                conn, addr = self.listeningSocket.accept()
                conn_mngr = connection_manager(conn,self.json_creator,self.logger,i,addr)
                conn_mngr.start()
                i += 1
            print("This will never get triggered, but has to be here because of python")
        except Exception as e:
            self.logger.error(e)
        finally:
            self.close()
    def close(self):
        self.listeningSocket.close()

class phantom:
    def __init__(self):
        plugin_id = 10892
        bstats(plugin_id).start()

        config_path = "config"
        is_config = True
        config_retriever = yaml_manager(defaultConfig,config_path,is_config)
        config = config_retriever.get_yml()
    
        phantomServer = server(config)
        phantomServer.start()
    
    def start(self):
        while(True):
            command = input()
            if command.lower() == "stop" or "exit":
                break;



phantom().start()
