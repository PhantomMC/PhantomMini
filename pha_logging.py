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


logname = "console"

def list_to_string(alist):
    output = ""
    for item in alist:
        if type(item) is bytes:
            try:
                item = str(item.decode("utf8"))
            except:
                item = str(item)
        elif type(item) is not str:
            item = str(item)
        
        output = output + " " + item
        
    return output

def generate_n_char(n,achar):
    output = achar;
    for i in range(n-1):
        output = output+achar
        
    return output
        
def write_time():
    return strftime("%y.%m.%d@%H:%M", localtime())


class logger:
    def __init__(self,version,config):
        if not os.path.exists("log"):
            os.mkdir("log")
        self.load_config(config)
        if self.is_store_users:
            default_yml = {}
            file_desti = "userList"
            self.user_data_manager = pha_yaml.yaml_manager(default_yml,file_desti)
            print("ping1")
            self.user_data = self.user_data_manager.get_yml()
        print("ping6")
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
        self.create_new_log()
        row1 = "----------------------\n"
        row2 = "|   Phantom server   |\n"
        row3 = "|   Version " + version + generate_n_char(9-len(version)," ")+"|\n"
        row4 = "----------------------\n"
        row5 = "[debug = " + str(self.is_debug) + ", style = " + str(config["Style"])+"]\n"
        msg =  row1 + row2 + row3 + row4 + row5
        self.display_msg(msg)
        
    def load_config(self,config):
        self.is_log_pings = self.to_boolean(config["Logging"]["storeMessages"])
        self.is_store_users = self.to_boolean(config["Logging"]["storeUsers"])
        self.is_debug = self.to_boolean(config["debug"])
        self.file_path = "log"
        
    def display_msg(self, msg):
        print(msg)
        self.write_to_file(msg)
        
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
    
    def register_user(self,client_port,client_address,client_username):
        msg = "from " + str(client_address) + ":" + str(client_port)
        
        if client_username is not None:
            msg = "Connection as " + client_username.decode("utf8") +" "+ msg
            self.info(msg)
            return
        
        self.debug("Connection "+msg)
        
    def create_new_log(self):
        if path.exists(self.file_path+"/"+logname+".log"):
            self.rename_old_log()
    def rename_old_log(self):
        i = 1
        while path.exists(self.file_path+"/"+logname+ str(i) +".old"):
            i += 1
        os.rename(self.file_path+"/"+logname+".log", self.file_path+"/"+logname+ str(i) +".old")
        
    def write_to_file(self,msg):
        if not self.is_log_pings:
            return
        
        with open(self.file_path + "/"+logname+".log","a") as file:
            file.write(msg + "\n")
            pass
            
    
    
    