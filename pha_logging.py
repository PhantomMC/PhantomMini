# -*- coding: utf-8 -*-
"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
"""
from time import gmtime, strftime

debug = True

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
def info(*msg):
    end_msg = list_to_string(msg)
    print("["+ strftime("%H:%M:%S", gmtime())+"]" + "  INFO",end_msg)
    
def debug(*msg):
    if debug:
        print("["+ strftime("%H:%M:%S", gmtime())+"]" + " DEBUG",list_to_string(msg))
        
        
class logger:
    def __init__(self,version):
        print("----------------------")
        print("|   Phantom server   |")
        print("|   Version " + version +"    |")
        print("----------------------")
        
    
    def register_ping(self,client_port,client_address):
        code = True
    
        

    
    