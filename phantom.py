"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
"""
import socket
import struct
import json
import time

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

class StatusPing:
    
    def __init__(self, host='localhost', port=25565, timeout=5):
        """ Init the hostname and the port """
        self._host = host
        self._port = port
        self._timeout = timeout
        
        
    
    
    



