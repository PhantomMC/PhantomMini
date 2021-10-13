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
import _thread
import time

Version = "0.7.14"
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


class pha_server(threading.Thread):
    def __init__(self):
        config_path = "config"
        is_config = True
        config_retriever = yaml_manager(defaultConfig, config_path, is_config)
        self.config = config_retriever.get_yml()
        self.host = self.config["serverInfo"]["host"]
        self.port = int(self.config["serverInfo"]["port"])
        self.serverSocket = self.getServerSocket()
        self.logger = logger(Version,self.config)
        self.json_creator = json_creator(self.config,self.logger)
        
        plugin_id = 10892
        bstats(plugin_id, self.logger, self.config).start()
        self.logger.debug("host:", self.host, "port", self.port)
        
    def getServerSocket(self):
        tryAmount = 5
        tryWait = 16 # s
        for i in range(tryAmount):
            try:
                serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                addr_info = socket.getaddrinfo(self.host, self.port)
                serverSocket.bind(addr_info[0][-1])
                return serverSocket
            except OSError:
                msg = "Port is already in use"
                if not hasattr(self, 'logger'):
                    print(msg)
                else:
                    self.logger.warning(msg)
                time.sleep(tryWait)
                tryWait *= 2
        
    def run(self):
        currentServerSocket = self.serverSocket
        restart = False
        try:
            i = 1
            while True:
                currentServerSocket.listen(0)
                (conn, addr) = currentServerSocket.accept()
                conn_mngr = connection_manager(conn,self.json_creator,self.logger,i,addr)
                self.logger.debug("Addres:",self.getIpAddress(addr))
                conn_mngr.start()
                i += 1
            print("This will never get triggered, but has to be here because of python")
        except OSError as e:
            restart = True
            self.logger.error(e)
                
        except Exception as e:
            self.logger.error(e)
        finally:
            try:
                currentServerSocket.close()
            except AttributeError:
                pass
            except:
                self.logger.warning("Unable to close port")
        if restart:
            self.serverSocket = self.getServerSocket()
            self.run()
        
    def stop(self):
        try:
            self.serverSocket.close()
        except AttributeError:
            pass
    @staticmethod
    def getIpAddress(rawAddress):
        ipAddres = ""
        i = 12
        for rawByte in rawAddress:
            part = rawByte & 255
            ipAddres = ipAddres + str(part)
            i -= 1
            if(i > 0):
                ipAddres = ipAddres + "."
                
        return ipAddres
            
class phantom:
    def __init__(self):
        self.startServer()
        
    def acceptCommands(self):
        while(True):
            command = input()
            if (command.lower() == "stop") or ("exit" == command.lower()):
                self.phantom_server.stop()
                break;
            if command.lower() is "restart":
                self.phantom_server.stop()
                self.phantom_server.stop
                self.startServer()
                continue
            
            print("unknown command")
        
    def startServer(self):
        self.phantom_server = pha_server()
        self.phantom_server.start()
        
        
phantomServer = phantom()
phantomServer.acceptCommands()
