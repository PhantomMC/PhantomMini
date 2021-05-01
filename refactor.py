# -*- coding: utf-8 -*-
"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
"""

class YamlParser:
    def __init__(self,file):
        self.linecount = 0
        self.allLines = file.readlines(  )
        self.block_type_switch = {
            dict : self.parse_block,
            list : self.parse_list,
            }
        self.string_parse_switch = {
            '"' : self.parse_from_bracket,
            "'" : self.parse_from_bracket,
            "[" : self.parse_list_from_string,
            "{" : self.parse_dict_from_string,
            "" : self.parse_unknown_from_string,
            }
        
    def parse_unknown_from_string(self, found_pos, type_starter, astring):
        found_pos = 0
        (endpos, theChar) = self.find(astring, ",")
        if(endpos == -1):
            endpos = len(astring)
        endstring = astring[found_pos:endpos]
        return (endpos, YamlParser.trim(endstring))
    
    def parse_dict_from_string(self,found_pos, type_starter, astring):
        astring = astring[found_pos:]
        adict = {}
        endpos = 0
        while True:
            (keyname, block_data, lastpos) = self.concat_linesegment(astring)
            adict[keyname] = block_data
            astring = astring[(lastpos+1):]
            (found_pos, found_char) = self.find(astring,[",", "}"])
            if(found_char == "}"):
                break
            
            astring = astring[(found_pos+1):]
        return (endpos, adict)
            
    def parse_list_from_string(self,start_pos,type_starter,astring):
        astring = astring[start_pos:]
        alist = []
        endpos = 0
        while True:
            (found_pos, found_char) = self.find(astring,[",", "]"])
            if(found_char == "]"):
                endpos = found_pos
                break;
            found_pos += 1
            (endpos, data) = self.parse_type_from_string(astring[:found_pos])
            astring = astring[(endpos+1):]
            alist.append(data)
            
            
        return (endpos+1, alist)
        
    def parse_from_bracket(self,found_pos,type_starter,astring):
        astring = astring[(found_pos+1):]
        (endpos, foundchar) = self.find(astring,type_starter)
        return (endpos, astring[:endpos])
    
    def parse_type_from_string(self,astring):
        starter_identifiers = self.string_parse_switch.keys()
        (found_pos, first_found_char)= self.find(astring,starter_identifiers)
        data_decoder = self.string_parse_switch[first_found_char]
        (endpos, data) = data_decoder(found_pos, first_found_char, astring)
        return (endpos, data)
    
    def parseline(self,line):
        (indent, line) = self.calc_indent(line)
        atomic = ""
        commentpos = len(line)
        # TODO, this is a poor temporary solution
        for i in range(len(line)):
            char = line[i]
            if (atomic != "") and (char == atomic):
                atomic = ""
                continue
            if char in ("'", '"'):
                atomic = char
                continue
            if (char == "#") and (atomic == ""):
                commentpos = i
                break
            if (char == "|") and (atomic == ""):
                return (indent, line[:i] 
                        + '"' 
                        + self.parse_stringsection(indent+2) 
                        + '"')
            
        return (indent, line[:commentpos])
    
    def undreadline(self):
        self.linecount -= 1
        
    def readline(self):
        if(self.linecount >= len(self.allLines)):
            return None
        line = self.allLines[self.linecount]
        exludingNewline = len(line) - 1
        self.linecount += 1
        return line[:exludingNewline]
        
    def parse_stringsection(self, target_indent):
        endstring = ""
        while True:
            (indent, line) = self.calc_indent(self.readline())
            if(line == "") or indent != target_indent:
                return endstring
            if(endstring != ""):
                endstring = endstring + "\n"
            endstring = endstring + line
        
    def readlinesegment(self):
        linesegment = ""
        while(linesegment == ""):
            line = self.readline()
            if(line == None):
                self.currentLine = None
                return 0
            (indent, linesegment) = self.parseline(line)
            
        self.currentLine = linesegment
        return indent
    
    @staticmethod
    def simple_split(astring, target_char):
        (pos, char) = YamlParser.find(astring, target_char)
        if(pos == -1):
            return (astring, None)
        return (astring[:pos], astring[(pos+1):])
    
    @staticmethod
    def calc_indent(aline):
        indent = 0
        for i in range(len(aline)):
            indent = i
            if(aline[indent] != " "):
                return (indent, aline[indent:])
            
        return (indent, "")
    
    @staticmethod
    def find(astring,target_chars):
        for i in range(len(astring)):
            if astring[i] in target_chars:
                return (i, astring[i])
        return (-1, "")
    
    @staticmethod
    def trim(astring):
        (indent, relevantString) = YamlParser.calc_indent(astring)
        return relevantString
    
    def detect_block_type(self,line):
        if line.startswith("- "):
            return list
        return dict
        
    def concat_linesegment(self,linesegment):
        (keyname, non_key_str) = self.simple_split(linesegment, ":")
        if (YamlParser.trim(non_key_str) == ""):
            indent = self.readlinesegment()
            block_type = self.detect_block_type(self.currentLine)
            block_data_decoder = self.block_type_switch[block_type]
            block_data = block_data_decoder(indent)
            endpos = 0
        else:
            (endpos, block_data) = self.parse_type_from_string(non_key_str)
            
        return (keyname, block_data, endpos)
    
    def parse_list(self,target_indent):
        indent = target_indent
        end_list = []
        while self.currentLine.startswith("- ") and (indent == target_indent):
            self.currentLine = self.currentLine.replace("- ", "  ", 1)
            (endpos, data) = self.parse_type_from_string(self.currentLine)
            end_list.append(data)
        self.undreadline()
        return end_list
    
    def parse_block(self,target_indent):
        adict = {}
        
        indent = target_indent
        while self.currentLine is not None and (indent >= target_indent):
            (keyname, data, endpos) = self.concat_linesegment(self.currentLine)
            adict[keyname] = data
            indent = self.readlinesegment()
        self.undreadline()
        return adict
        
    def parse(self):
        indent = self.readlinesegment()
        adict = self.parse_block(indent)
        return adict
    
    
def dump(data, stream, sort_keys=True, indent=0):
    def do_indent(indent):
        stream.write("  " * indent)

    if isinstance(data, list):
        for i in data:
            do_indent(indent - 1)
            stream.write("- ")
            dump(i, stream, sort_keys, indent + 1)
    elif isinstance(data, dict):
        it = data.items()
        if sort_keys:
            it = sorted(it)
        for k, v in it:
            do_indent(indent)
            stream.write(str(k))
            if isinstance(v, (list, dict)):
                stream.write(":\n")
                dump(v, stream, sort_keys, indent + 1)
            else:
                stream.write(": ")
                dump(v, stream, sort_keys, indent + 1)
    else:
        stream.write(str(data))
        stream.write("\n")