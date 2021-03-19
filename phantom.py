"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
 
 
 Version 0.1.0
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
        "text": "foo",
        "bold": "true",
        "extra": [
        {"text": "bar"},
        
        {"text": "baz",
         "bold": "false"},
        
        {"text": "qux",
         "bold": "true"}
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
def pack_data(data):
        """ Page the data """
        if type(data) is str:
            data = data.encode('utf8')
            return pack_varint(len(data)) + data
        elif type(data) is int:
            return struct.pack('H', data)
        elif type(data) is float:
            return struct.pack('L', int(data))
        else:
            return data

def unpack_varint(conn):
        """ Unpack the varint """
        data = 0
        for i in range(5):
            ordinal = conn.recv(1)

            if len(ordinal) == 0:
                print("pong",i)
                break

            byte = ord(ordinal)
            data |= (byte & 0x7F) << 7*i

            if not byte & 0x80:
                print("ping", i)
                break
        
        print(data)
        return data


def read_fully(connection):
        """ Read the connection and return the bytes """
        packet_length = unpack_varint(connection)
        
        if packet_length == 1:
            return None
        
        byte = connection.recv(packet_length)

        return byte


def start():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            for i in range(0,3):
                data = read_fully(conn)
                print(data)
                print("next")
                if data is None:
                    conn.sendall(pack_data(json.dumps(JSON_Response)))
                    
                    
                
                
            
start()

        
    
    
    
    



