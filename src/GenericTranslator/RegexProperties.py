'''
@author: Nico57c
'''
__all__ = ["RegexProperties", "RegexGt"]

import re
import configparser
import os.path


class RegexGt(object):
    '''
    Value of regex for Generic Translator
    '''
    _value = None
    flag = re.IGNORECASE
    defaultTag = None

    def __init__(self, value, flag = re.IGNORECASE):
        self._value = value
        self.flag = flag

    def value(self, tagKey=None):
        if(None!=tagKey):
            return self._value.replace('tagStart', tagKey['start']).replace('tagEnd', tagKey['end'])
        elif(None!=self.defaultTag):
            return self._value.replace('tagStart', self.getDefaultTagValue('start')).replace('tagEnd', self.getDefaultTagValue('end'))
        else:
            return self._value

    def setDefaultTag(self, start, end):
        self.defaultTag = { 'start': start, 'end': end }
        return self

    def getDefaultTagValue(self, index):
        return self.defaultTag[index].value()

    def flag(self):
        return self.flag

    def compile(self):
        return re.compile(self.value(), self.flag)

    def findall(self, text):
        return re.findall(self.value(), text, self.flag)



class RegexProperties(object):
    '''
    Load / Write regex properties for Translator usage.
    '''
    path = None
    configFile = None
    section = 'regex'

    def __init__(self, path=None):
        self.configFile = configparser.ConfigParser()
        self.configFile.add_section(self.section)
        self.path = path

    def load(self, path=None):
        self.path = path if(path!=None) else self.path
        if(self.path == None):
            raise FileNotFoundError('RegexProperties.load need path parameter.')
        if(os.path.exists(self.path)):
            self.configFile.remove_section(self.section)
            self.configFile.read(self.path, encoding='utf-8')
            if(False==self.configFile.has_section(self.section)):
                self.configFile = None
                raise Exception('Section ' + self.section + ' not found in RegexProperties file : ' + self.path)
        else:
            raise FileNotFoundError('RegexProperties.load file not found ' + self.path)

    def save(self):
        self.configFile.write(open(self.path, 'w', encoding='UTF-8', newline='\n'))

    def getRegex(self, name, default=None):
        if(False == self.configFile.has_option(self.section, name)):
            self.configFile.set(self.section, name, default)
            return default
        else:
            return self.configFile.get(self.section, name)

    def printAll(self):
        for item in sorted(self.configFile.items()):
            print(item)

