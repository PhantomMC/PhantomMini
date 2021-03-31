# -*- coding: utf-8 -*-
"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
"""
from time import gmtime, strftime
import os
from os import path


def list_to_string(alist):
    output = ""
    for item in alist:
        if type(item) is bytes:
            try:
                item = item.decode("utf8")
            except:
                item = str(item)
        elif type(item) is not str:
            item = str(item)
        output = output + " " + item
        
    return output

        
        
class logger:
    def __init__(self,version,config):
        
        if not os.path.exists("log"):
            os.mkdir("log")
        
        self.log_pings = config["Logging"]["pings"]["log"]
        self.is_debug = config["debug"]
        self.file_path = "log"
        self.create_new_log()
            
        msg =   "----------------------\n" + "|   Phantom server   |\n"+"|   Version " + version +"    |\n"+"----------------------"
        print (msg)
        self.write_to_file(msg)
        msg = "[debug = " + str(self.is_debug) + ", style = " + str(config["Style"])+"]\n"
        print(msg)
        self.write_to_file(msg)
        
    def info(self,*msg):
        end_msg = "["+ strftime("%H:%M:%S", gmtime())+" INFO ] " + list_to_string(msg)
        
        print(end_msg)
        self.write_to_file(end_msg)
    
    def debug(self,*msg):
        if self.is_debug:
            end_msg = "["+ strftime("%H:%M:%S", gmtime())+" Debug]" + list_to_string(msg)
            self.write_to_file(end_msg)
            print(end_msg)
        
    def register_ping(self,client_port,client_address):
        self.debug("Connected to",client_address,"at port",client_port)
        
        
    def create_new_log(self):
        if path.exists(self.file_path+"/pings.log"):
            self.rename_old_log()
    def rename_old_log(self):
        i = 1
        while path.exists(self.file_path+"/pings"+ str(i) +".old"):
            i += 1
        os.rename(self.file_path+"/pings.log", self.file_path+"/pings"+ str(i) +".old")
        
    def write_to_file(self,msg):
        if not self.log_pings:
            return
        
        with open(self.file_path + "/pings.log","a") as file:
            file.writelines(msg + "\n")
    
    