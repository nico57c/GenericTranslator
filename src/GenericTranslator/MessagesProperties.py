'''
@author: Nico57c
'''
__all__ = ["MessagesProperties"]

import configparser
import os.path
from GenericTranslator.RegexProperties import RegexGt

class MessagesProperties(object):
    '''
    Messages recorded in properties file.
    '''
    path = None
    configFile = None
    section = None
    regex = None
    temp = {}

    def __init__(self, regex: RegexGt, path=None, language='default'):
        self.configFile = configparser.ConfigParser()
        self.section=language
        self.path = path
        self.regex = regex

    def load(self, path=None):
        self.path = path if(path!=None) else self.path
        if(self.path == None):
            raise FileNotFoundError('MessagesProperties.load need path parameter.')
        if(os.path.exists(self.path)):
            self.configFile.read(self.path, encoding='utf-8')
            if(False==self.configFile.has_section(self.section)):
                self.configFile = None
                raise Exception('Section ' + self.section + ' not found in MessagesProperties file : ' + self.path)
        else:
            raise FileNotFoundError('MessagesProperties.load file not found ' + self.path)

    def save(self):
        self.configFile.write(open(self.path, 'w', encoding='UTF-8', newline='\n'))

    def printAll(self):
        for item in sorted(self.configFile.items()):
            print(item)


    def message(self, name, default=None, parameters=None):
        if(None==parameters):
            if(None == self.configFile.get(self.section, name)):
                self.configFile.set(self.section, name, default if(default != None) else name)
                return default if(default != None) else name
            else:
                return self.configFile.get(self.section, name)

        else:
            self.temp['parameters'] = parameters
            return self.regex.compile().sub(self._replaceParameter, self.message(name))

    # private for parameter replacement :
    def _replaceParameter(self, matchObj):
        if(None != self.temp['parameters'][matchObj.group(2)]):
            glue = " " if(None == matchObj.group(4)) else matchObj.group(4)
            return glue.join(self.temp['parameters'][matchObj.group(2)])
        else:
            return matchObj.groups()

