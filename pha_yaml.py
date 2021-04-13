# -*- coding: utf-8 -*-
"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
"""

import os
import uyaml
class yaml_manager:
    def __init__(self,default_YML,file_desti,is_config = False):
        self.file_desti = file_desti
        self.is_config = is_config
        self.default_YML = default_YML
        self.is_micropython = False
    def _try_get_yml(self):
        if os.path.exists(self.file_desti + ".yml"):
            return self._load_yml()
        else:
            print("No " + self.file_desti + " was found, providing a new one")
            self.write_yml(self.default_YML)
            return False
            
    def _load_yml(self):
        try:
            file = open(self.file_desti + ".yml",encoding = "utf8")
        except:#for micropython
            file = open(self.file_desti + ".yml")
            self.is_micropython = True
            
        try:
            self.yml_dictionary = self.load(file)
            print(self.yml_dictionary)
            file.close()
            if self.is_config and (int(self.yml_dictionary["configVersion"]) != self.default_YML["configVersion"]):
                return self._rename_config()
            return True
        except Exception as e:
            print(e)
            file.close()
        return False
            
    def _rename_config(self):
        print("Providing you with a newer (and shittier) config")
        old_desti = self.file_desti + ".old"
        if os.path.exists(old_desti):
            os.remove(old_desti)
        os.rename(self.file_desti + ".yml", old_desti)
        return self.write_yml()
            
    def write_yml(self,yml):
        try:
            file = open(self.file_desti + ".yml","w+")
            self.write(file,self.default_YML)
        except:
            file.close()
            return False
        finally:
            file.close()
        return True
    
    def get_yml(self):
        if not self._try_get_yml():
            return None
        return self.yml_dictionary
    
    def load(self,file_stream):
        return uyaml.YamlParser(file_stream).parse()
        
    def write(self,afile,adictionary):
        uyaml.dump(adictionary,afile)
