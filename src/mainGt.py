'''
@author: Nico57c
'''
import sys
import os.path
import codecs
import getopt
import imp
from GenericTranslator.GenericTranslator import GenericTranslator
from configparser import ConfigParser

class MainGt(object):

    @staticmethod
    def help():
        print(
'Help screen (-r -m -l -i required) :\n\
 -e, --extract Extract messages name from input file to output\n\
 -t, --translate Translate input file (default)\n\
 -r, --regex File path of "regex.properties" config file\n\
 -m, --messages File path of "messages.properties" translator file\n\
 -l, --language fr|de|en|... (section of you want in message file for translation)\t\tLanguage of translate\n\
 -i, --input File path of input file\n\
 -o, --ouput File path of output file (encoding : UTF-8, newline: UNIX)\n\
 -h, --help\t\t\tDisplay this screen\n')
        sys.exit()

    @staticmethod
    def params():
        parameters = {'regex':None, 'messages':None, 'language':None, 'input':None, 'output':None, 'extract':False, 'plugin':None}
        opts, args = getopt.getopt(sys.argv[1:], 'hr:m:l:i:o:tep:', ['help', 'regex=', 'messages=', 'language=', 'input=','output=', 'translate', 'extract', 'plugin='])
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                MainGt.help()
                sys.exit()
            elif opt in ("-r", "--regex"):
                parameters['regex'] = arg
            elif opt in ("-m", "--messages"):
                parameters['messages'] = arg
            elif opt in ("-l", "--language"):
                parameters['language'] = arg
            elif opt in ("-i", "--input"):
                parameters['input'] = arg
            elif opt in ("-o", "--output"):
                parameters['output'] = arg
            elif opt in ("-t", "--translate"):
                parameters['extract'] = False
            elif opt in ("-e", "--extract"):
                parameters['extract'] = True
            elif opt in ("-p", "--plugin"):
                parameters['plugin'] = arg

        if(parameters['messages']==None or parameters['language']==None or parameters['input']==None):
            print('More arguments needs.\n\n')
            MainGt.help()
        return parameters

    @staticmethod
    def run():
        try:
            parameters = MainGt.params()
            gt = GenericTranslator(regexPropertiesPath = parameters['regex'], 
                                   messagesPropertiesPath = parameters['messages'], 
                                   language = parameters['language'])

            output = None
            if(os.path.exists(parameters['input'])):
                with open(parameters['input'], 'r', encoding='utf-8', newline='\n') as inputFile:
                    if(False == parameters['extract']):
                        output = gt.translate(inputFile.read())
                    else:
                        output = gt.extractLabels(inputFile.read())
                    inputFile.close()
            else:
                print('Input file does not exists!')
                sys.exit()

            if(output!=None):
                if(None!=parameters['output'] and False == parameters['extract']):
                    with open(parameters['input'], 'w', encoding='utf-8', newline='\n') as outputFile:
                        outputFile.write(output)
                        outputFile.close()
                elif(None!=parameters['output'] and True == parameters['extract']):
                    with open(parameters['input'], 'w', encoding='utf-8', newline='\n') as outputFile:
                        outputMessages = ConfigParser()
                        outputMessages.read_file(outputFile)
                        outputMessages.add_section(parameters['language'])
                        for label in output:
                            outputMessages.set(parameters['language'], label, parameters['language'] + ' + ' + label)
                        outputMessages.write(outputFile)
                else:
                    if(None!=parameters['plugin']):
                        MainGt.callPlugin(parameters['plugin'], output=output, parameters=parameters)
                    else:
                        print(output)
            else:
                print('An error occured!')

        except FileNotFoundError as error:
            print("An error occured!\n%s" % error)

    @staticmethod
    def loadPlugin(filepath):
        class_inst = None
        mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])
        if file_ext.lower() == '.py':
            py_mod = imp.load_source(mod_name, filepath)
        elif file_ext.lower() == '.pyc':
            py_mod = imp.load_compiled(mod_name, filepath)
        if hasattr(py_mod, 'Plugin'):
            class_inst = getattr(py_mod, 'Plugin')()
        return class_inst


    @staticmethod
    def callPlugin(filePath, output=None, parameters=None):
        plugin = MainGt.loadPlugin(filePath)
        plugin.run(output=output, parameters=parameters)

MainGt.run()
