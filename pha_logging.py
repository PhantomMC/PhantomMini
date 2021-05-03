# -*- coding: utf-8 -*-
"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
"""
from time import strftime, localtime
import os
from os import path
import pha_yaml
import refactor as yaml


logname = "console"
userlistname = "userList"
logFolderName = "log"

def list_to_string(alist):
    output = ""
    for item in alist:
        if type(item) is bytes:
            try:
                item = str(item.decode("utf8"))
            except:
                item = str(item)
        if type(item) is Exception:
            item = type(item) + "\n" + item.args + "\n" + item
        elif type(item) is not str:
            item = str(item)
        
        output = output + " " + item
        
    return output
        
def write_time():
    return strftime("%y.%m.%d@%H:%M", localtime())


class logger:
    def __init__(self,version,config):
        if not os.path.exists(logFolderName):
            os.mkdir(logFolderName)
        self.load_config(config)
        if self.is_store_users:
            default_yml = {}
            file_desti = logFolderName + "/" + userlistname + ".yml"
            self.user_data_manager = pha_yaml.yaml_manager(default_yml,file_desti)
            self.user_data = self.user_data_manager.get_yml()
        self.print_ini_msg(version,config)
    
    @staticmethod
    def to_boolean(astring):
        astring = astring.lower()
        if(astring == "true"):
            return True
        if(astring == "false"):
            return False
        raise ValueError("Unable to convert string to boolean")
        
    def print_ini_msg(self,version,config):
        msg = "<Initializing Phantom server Version " + version + ">"
        self.display_msg(msg)
        
    def load_config(self,config):
        self.is_log_pings = self.to_boolean(config["Logging"]["storeMessages"])
        self.is_store_users = self.to_boolean(config["Logging"]["storeUsers"])
        self.is_debug = self.to_boolean(config["debug"])
        
    def display_msg(self, msg):
        print(msg)
        self.log_line(msg)
        
    def info(self,*msg):
        end_msg = write_time() + " [INFO]" + list_to_string(msg)
        self.display_msg(end_msg)
        
    
    def debug(self,*msg):
        if self.is_debug:
            end_msg = write_time() +" [DEBUG]" + list_to_string(msg)
            self.display_msg(end_msg)
    
    def error(self, *msg):
        end_msg = write_time() + " [ERROR]" + list_to_string(msg)
        self.display_msg(end_msg)
    def warning(self, *msg):
        end_msg = write_time() + " [WARNING]" + list_to_string(msg)
        self.display_msg(end_msg)
    def register_user(self,client_port,client_address,client_username):
        msg = "from " + str(client_address) + ":" + str(client_port)
        
        if client_username is not None:
            str_username = client_username.decode("utf8")
            msg = "Connection as " + str_username +" "+ msg
            self.info(msg)
            self.log_user_join(str_username, str(client_address))
            return
        
        self.debug("Connection "+msg)
    
    def log_line(self, msg):
        if not self.is_log_pings:
            return
        
        with open(logFolderName + "/"+logname+".log","a") as file:
            file.write(msg + "\n")
            
    def log_user_join(self, username, ip):
        if not self.is_store_users:
            return
        #TODO : this solution does not bode well for multiple threads
        fileLocation = logFolderName + "/" + userlistname + ".yml"
        currentDict = {}
        with open(fileLocation, "a") as readStream:
            yaml_parser = yaml.YamlParser(readStream)
            currentDict = yaml_parser.parse()
            usernames = currentDict.keys()
            if username in usernames:
                currentDict[username]["joinAmount"] += 1 
            else:
                userDict = {"joinAmount" : 1}
                currentDict[username] = userDict
            
        with open(fileLocation, "w") as overWriteStream:
            yaml_parser.dump(currentDict, overWriteStream)