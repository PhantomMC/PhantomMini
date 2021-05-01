# -*- coding: utf-8 -*-
"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
"""
import struct
import threading
from time import sleep
class connection_manager(threading.Thread):
    
    def __init__(self,conn,ajson_creator,logger,threadID,addr):
        
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.json_creator = ajson_creator
        self.conn = conn
        self.logger = logger
        #recieve handshake
        packet_length = self.unpack_varint();
        self.packet_id = self.unpack_varint() #TODO check if invalid
        self.protocol_version = self.unpack_varint()
        print( self.unpack_string() )
        self.read_data(2)
        self.state = self.unpack_varint()
        self.username = None
        
        
        self.client_address = addr[0]
        print(addr[0])
        self.client_port = addr[1]
        
    def write_data(self,data):
        self.conn.sendall(data)
    def read_data(self,length):
        return self.conn.recv(length)
        
    def pack_varint(self,data):
         """ Pack the var int """
         ordinal = b''
         while True:
             byte = data & 0x7F
             data >>= 7
             ordinal += struct.pack('B', byte | (0x80 if data > 0 else 0))
    
             if data == 0:
                 break
    
         return ordinal
     
    def unpack_string(self):
        string_length = self.unpack_varint()
        return self.read_data(string_length)
    def pack_string(self,astring):
        data = astring.encode('utf8')
        return self.pack_varint(len(data)) + data
    
    def write_response(self):
        self.json_creator.change_Response_dictionary(self.protocol_version)
        response = b'\x00' + self.pack_string(self.json_creator.get_JSON_string())
        return  self.pack_varint(len(response)) + response
    
    def unpack_varint(self):
        """ Unpack the varint """
        data = 0
        for i in range(5):
            ordinal = self.read_data(1)

            if len(ordinal) == 0:
                break

            byte = ord(ordinal)
            data |= (byte & 0x7F) << 7*i

            if not byte & 0x80:
                break
        return data
    
    def read_fully(self):
        """ Read the connection and return the bytes """
        packet_length = self.unpack_varint()
        byte = self.read_data(packet_length)
 
        return byte
    def do_response(self):
        if(self.state == 1):
            self.status_connection()
            return
        if(self.state == 2):
            self.login_connection()
        
    def status_connection(self):
        while True:
            data = self.read_fully()
            self.logger.debug("Recieved",data)
            if data == b'\x00':
                self.write_data(self.write_response())
                self.logger.debug("Sent JSON response")
            elif data == b'':
                break
            else:
                self.write_data(self.pack_varint(len(data)) + data)
                self.logger.debug("Responded to ping with:",data)
                break
    
    def interpret_login(self):
        packet_length = self.unpack_varint()
        self.packet_id = self.unpack_varint()
        self.username = self.unpack_string()
    
    def compile_disconnect_data(self):
        chat_data = self.pack_string(self.json_creator.get_disconnect_dictionary_string())
        full_data = b'\x00' + chat_data
        return self.pack_varint(len(full_data)) + full_data
    
    def login_connection(self):
        recieved_data = self.interpret_login()
        self.logger.debug("Recieved",str(recieved_data))
        final_data = self.compile_disconnect_data();
        self.logger.debug("Sent JSON disconnect message")
        self.write_data(final_data)
    
    def register_event(self):
        self.logger.register_user(self.client_port, self.client_address, self.username)
        
    def run(self):
        try:
            sleep(1)
            self.do_response()
            self.register_event()
        finally:
            self.conn.close()