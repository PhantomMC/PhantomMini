"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
 
 
 Version 0.1.3
"""
import socket
import json
import struct
JSON_Response = {
    "version": {
        "name": "1.16.5",
        "protocol": 754
    },
    "players": {
        "max": 0,
        "online": 0,
        "sample": []
    },
    "description": {
        "text": "Locked",
        "bold": "true",
        "extra": [
        
        {"text": "Craft",
         "bold": "false"}
        ]
    },
    "favicon": "data:image/png;base64,<data>"
}


host='localhost'
port=25565
timeout=5

def pack_varint(data):
     """ Pack the var int """
     ordinal = b''
     while True:
         byte = data & 0x7F
         data >>= 7
         ordinal += struct.pack('B', byte | (0x80 if data > 0 else 0))

         if data == 0:
             break

     return ordinal


def write_response():
    json_data = json.dumps(JSON_Response).encode('utf8')
    print(len(json_data))
    return  pack_varint(len(json_data)+3) + b'\x00' + pack_varint(len(json_data)) + json_data

def unpack_varint(conn):
        """ Unpack the varint """
        data = 0
        for i in range(5):
            ordinal = conn.recv(1)

            if len(ordinal) == 0:
                break

            byte = ord(ordinal)
            data |= (byte & 0x7F) << 7*i

            if not byte & 0x80:
                break
        print(data)
        return data


def read_fully(connection):
        """ Read the connection and return the bytes """
        packet_length = unpack_varint(connection)
        
        byte = connection.recv(packet_length)

        return byte

def connection_actions(conn):
    try:
        data = read_fully(conn)#accept handshake
        print(data)
        print("-------")
        for i in range(0,2):
            data = read_fully(conn)
            print("recieved data:",data)
            if data == b'\x00':
                conn.sendall(write_response())
                print("Sending:", write_response())
            else:
                conn.sendall(pack_varint(len(data)+1) + data)
                print("Sending",pack_varint(len(data)+1)+data)
            print("-------")
    finally:
        conn.close()

def start():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        connection_actions(conn)
    finally:
        s.close()
                    
                
    
            
start()

        
    
    
    
    



