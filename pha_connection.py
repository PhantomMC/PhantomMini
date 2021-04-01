# -*- coding: utf-8 -*-
"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
"""
import struct

class connection_manager:
    
    def __init__(self,conn,ajson_creator,logger):
        self.json_creator = ajson_creator
        self.conn = conn
        self.logger = logger
        #recieve handshake
        packet_length = self.unpack_varint();
        self.packet_id = self.unpack_varint() #TODO check if invalid
        self.protocol_version = self.unpack_varint()
        self.client_address = self.unpack_string()
        self.client_port = self.read(2)
        self.state = self.unpack_varint()
        self.username = None
        self.logger.info("Connected to",self.client_address,"at port",struct.unpack("H", self.client_port))
        
    def write(self,data):
        self.conn.sendall(data)
    def read(self,length):
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
        return self.read(string_length)
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
            ordinal = self.read(1)

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
        byte = self.read(packet_length)
 
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
            self.logger.debug("Recieved",str(data))
            if data == b'\x00':
                self.write(self.write_response())
                self.logger.debug("Sent JSON response")
            elif data == b'':
                break
            else:
                self.write(self.pack_varint(len(data)) + data)
                self.logger.debug("Responded to ping.")
                break
    
    def interpret_login(self):
        packet_length = self.unpack_varint()
        self.packet_id = self.unpack_varint()
        self.username = self.unpack_string()
        self.logger.info(self.username , "tried to establish a connection")
    
    def compile_disconnect_data(self):
        chat_data = self.pack_string(self.json_creator.get_disconnect_dictionary_string())
        full_data = b'\x00' + chat_data
        return self.pack_varint(len(full_data)) + full_data
    
    def login_connection(self):
        recieved_data = self.interpret_login()
        self.logger.debug("Recieved",str(recieved_data))
        final_data = self.compile_disconnect_data();
        self.logger.debug("Sent JSON disconnect message")
        self.write(final_data)
    
    def register_event(self):
        self.logger.register_user(self.client_port, self.client_address, self.username)