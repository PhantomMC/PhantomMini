# -*- coding: utf-8 -*-
"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
"""
import struct
from pha_logging import send_message,debug

class connection_manager:
    
    def __init__(self,conn,ajson_creator):
        self.json_creator = ajson_creator
        self.conn = conn
        
        #recieve handshake
        packet_length = self.unpack_varint();
        self.packet_id = self.unpack_varint() #TODO check if invalid
        self.protocol_version = self.unpack_varint()
        string_length = self.unpack_varint()
        self.client_address = conn.recv(string_length)
        self.client_port = self.conn.recv(2)
        self.state = self.unpack_varint()
        
        send_message("Connected to",self.client_address,"at port",self.client_port)
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
            ordinal = self.conn.recv(1)

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
        byte = self.conn.recv(packet_length)
 
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
            if data == b'\x00':
                self.conn.sendall(self.write_response())
            elif data == b'':
                break
            else:
                self.conn.sendall(self.pack_varint(len(data)) + data)
                break
            
    def compile_disconnect_data(self):
        chat_data = self.pack_string(self.json_creator.get_disconnect_dictionary_string())
        full_data = b'\x00' + chat_data
        return self.pack_varint(len(full_data)) + full_data
    
    
    def login_connection(self):
        recieved_data = self.read_fully()
        
        final_data = self.compile_disconnect_data();
        
        self.conn.sendall(final_data)