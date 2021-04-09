# -*- coding: utf-8 -*-
"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
"""
from time import strftime, localtime
import os
import struct
from os import path


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
    return strftime("%H:%M:%S", localtime())
class logger:
    def __init__(self,version,config):
        
        if not os.path.exists("log"):
            os.mkdir("log")
        
        self.log_pings = config["Logging"]["log"]
        self.is_debug = config["debug"]
        self.file_path = "log"
        self.create_new_log()
        row1 = "----------------------\n"
        row2 = "|   Phantom server   |\n"
        row3 = "|   Version " + version + generate_n_char(9-len(version)," ")+"|\n"
        row4 = "----------------------\n"
        row5 = "[debug = " + str(self.is_debug) + ", style = " + str(config["Style"])+"]\n"
        msg =  row1 + row2 + row3 + row4 + row5
        print (msg)
        self.write_to_file(msg)
        
    def info(self,*msg):
        end_msg = "["+ write_time() +" INFO ]" + list_to_string(msg)
        
        print(end_msg)
        self.write_to_file(end_msg)
    
    def debug(self,*msg):
        if self.is_debug:
            end_msg = "["+ write_time() +" Debug]" + list_to_string(msg)
            self.write_to_file(end_msg)
            print(end_msg)
        
    def register_user(self,client_port,client_address,client_username):
        msg = "Registered action at adress " + client_address.decode("utf8") + " ,port " + str(struct.unpack("H", client_port))
        
        if client_username is not None:
            msg = msg + " with username " + client_username.decode("utf8")
        
        self.debug(msg)
        
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
    
    