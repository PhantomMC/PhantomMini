"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
 
 
 Version 0.3.0
"""
import socket
import json
import struct
import base64
import yaml;



defaultConfig = {
    "networking" : {
        "host" : "localhost",
        "port" : 754,
        "timeout" : 5
        },
    "graphics" : {
        "MOTD" : "This is a fake server",
        "DisconnectMessage" : "You_got_rickrolled",
        "png_image_link" : "logo.png",
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
        "version" : {
            "name" : "Test",
            "protocoll" : -1 ,
            }
        }
    
    }



try:
    config_file = open("config.yml")
except IOError:
    config_file = open("config.yml","w+")
    config_file.write(yaml.dump(defaultConfig))
try:
    config = yaml.load(config_file)
    print(config)
finally:
    config_file.close()



binary_file = open(config["png_image_link"])

try:
    binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode('utf-8')
finally:
    binary_file.close()
    

JSON_Response = {
    "version": {
        config["version"]
    },
    "players": {
        config["players"]
    },
    "description": {
        config["description"]
    },
    "favicon": "data:image/png;base64," + base64_message
}


host='localhost'
port=25565
timeout=5



def read_handshake(conn):
    packet_length = unpack_varint(conn);
    packet_id = unpack_varint(conn)
    protocol_version = unpack_varint(conn)
    string_length = unpack_varint(conn)
    client_address = conn.recv(string_length)
    client_port = conn.recv(2)
    state = unpack_varint(conn)
    return protocol_version,state
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
def pack_string(astring):
    data = astring.encode('utf8')
    return pack_varint(len(data)) + data

def write_response():
    json_string = json.dumps(JSON_Response)
    response = b'\x00' + pack_string(json_string)
    return  pack_varint(len(response)) + response

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

def status_connection(conn):
    while True:
        data = read_fully(conn)
        print("Recieved:",data)
        if data == b'\x00':
            conn.sendall(write_response())
            print("Sent: ", write_response())
        elif data == b'':
            break
        else:
            conn.sendall(pack_varint(len(data)) + data)
            print("Sending",pack_varint(len(data))+data)
            break

def compile_disconnect_data():
    chat_data = pack_string( config["DisconnectMessage"] )
    full_data = b'\x00' + chat_data
    return pack_varint(len(full_data)) + full_data

def login_connection(conn):
    
    recieved_data = read_fully(conn)
    
    print(recieved_data)
    
    final_data = compile_disconnect_data();
    
    print("final_data: ",final_data)
    conn.sendall(final_data)
    

def connection_actions(conn):
    try:
        print("-------")
        protocol_version,data = read_handshake(conn)
        print("Recieved hanshake with id:",data)
        print("-------")
        if data == 1:
            status_connection(conn)
        elif data == 2:
            login_connection(conn)
    finally:
        conn.close()

def start():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        while True:
            s.listen(1)
            conn, addr = s.accept()
            connection_actions(conn)
        
    finally:
        s.close()
                    
                
    
            
start()

        
    
    
    
    



