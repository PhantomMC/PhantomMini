"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
 
 
 Version 0.5.1
"""
import socket
import json
import struct
import base64
import yaml
import os
import re
defaultConfig = {
        "configVersion" : 1,
        "serverInfo" : {
            "host" : "localhost",
            "port" : 25565
        },
        "Style" : 1, #chose between 1, 2 and 3
        "Content" : {
            "lowerMessage" : "A message",
            "upperMessage": "This msg appears above the server!",
            "hoverMessage" : "You should have brought a config",
            "kickMessage" : "Angry",
            "imagePath" : "Logo.png"
        }
        
    }


while True:
    try:
        config_file = open("config.yml")
        config = yaml.load(config_file)
        print(config)
        if(config["configVersion"] != defaultConfig["configVersion"]):
            print("Providing you with a newer config")
            os.renames("config.yml", "config.yml.old")
            continue
        config_file.close()
        break
    except IOError:
        config_file = open("config.yml","w+")
        print("No config was found, provididing a shittier one")
        config_file.write(yaml.dump(defaultConfig))
        config_file.close()
    finally:
        config_file.close()


Content = config["Content"]
binary_file = open(Content["imagePath"],'rb')

try:
    binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode('utf-8')
except UnicodeDecodeError:
    print("Can't find image from imagepath")
finally:
    binary_file.close()
    

def JSON_Response(protocol_version):
    virtual_Playernames = re.split("\n", Content["hoverMessage"])
    
    virtual_players = []
    print(virtual_Playernames)
    for playername in virtual_Playernames:
        playerDict = {"name":fix_coloring(playername),"id": "4566e69f-c907-48ee-8d71-d7ba5aa00d20"}
        virtual_players.append(playerDict)
    
    max_players = 0
    if config["Style"] == 3:
        max_players = 1
    if config["Style"] == 1:
        protocol_version = -1;
        
    JSON = {
        "version" : {
            "name":fix_coloring(Content["upperMessage"]),
            "protocol":protocol_version
            },
        "players": {
            "max": max_players,
            "online": 0,
            "sample" : virtual_players},
        "description": fix_coloring(Content["lowerMessage"]),
        "favicon": "data:image/png;base64" + base64_message
        }
    return JSON
    


host='localhost'
port=25565
timeout=5

def fix_coloring(text):
    #TODO add a \& option
    return re.sub("&", "§", text)

def read_handshake(conn):
    packet_length = unpack_varint(conn);
    packet_id = unpack_varint(conn) #TODO check if invalid
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

def write_response(protocol_version):
    json_string = json.dumps(JSON_Response(protocol_version))
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

def status_connection(conn,protocol_version):
    while True:
        data = read_fully(conn)
        print("Recieved:",data)
        if data == b'\x00':
            conn.sendall(write_response(protocol_version))
            print("Sent: ", write_response(protocol_version))
        elif data == b'':
            break
        else:
            conn.sendall(pack_varint(len(data)) + data)
            print("Sending",pack_varint(len(data))+data)
            break

def compile_disconnect_data():
    chat_data = pack_string( Content["kickMessage"] )
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
            status_connection(conn,protocol_version)
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

        
    
    
    
    



