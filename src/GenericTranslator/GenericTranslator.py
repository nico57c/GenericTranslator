'''
@author: Nico57c
'''
__all__ = ["GenericTranslator"]

from GenericTranslator.RegexProperties import RegexProperties, RegexGt
from GenericTranslator.MessagesProperties import MessagesProperties


class GenericTranslator(object):
    '''
    Generic translator
    '''

    regexProperties = None
    re_gtTagStart = RegexGt("gt\(")
    re_gtTagEnd = RegexGt("\)")
    re_gtTagParamValue = RegexGt("strDel([^strDel]*)strDel[paramDel]{0,1}")
    re_gtTagStrDel = RegexGt("\\\"") # String delimiter
    re_gtTagParamDel = RegexGt("\\,") # Parameter delimiter
    re_gtTagParamAff = RegexGt("\\=") # Parameter affectation
    re_gtTagArOpen = RegexGt("\[") # Array open character
    re_gtTagArClose = RegexGt("\]") # Array end character
    re_gtTagTrans = RegexGt("tagStart([^tagEndparamDel]*)(?:.(?!tagStart)*)*[tagEnd]{1}")
    re_gtTagParam = RegexGt("([^paramAffparamDel\ ]*)[ ]*paramAff[ ]*[arClose]{0,1}[ ]*(strDel[^strDel]*strDel)[ ]*[arCloseparamDel]{0,1}")

    messageProperties = None
    re_mpTag = RegexGt("(\$\(([^\)]*)\))(\(([^\)]*)\))*")

    def __init__(self, regexPropertiesPath = None, messagesPropertiesPath=None, language=None):
        # Load regex from config file :
        self.regexProperties = RegexProperties()
        if(None != regexPropertiesPath):
            self.regexProperties.load(regexPropertiesPath)
        self.re_gtTagStart = RegexGt(self.regexProperties.getRegex('tagStart', self.re_gtTagStart.value()))
        self.re_gtTagEnd = RegexGt(self.regexProperties.getRegex('tagEnd', self.re_gtTagEnd.value()))
        self.re_gtTagParamValue = RegexGt(self.regexProperties.getRegex('paramValue', self.re_gtTagParamValue.value())).setDefaultTag(start=self.re_gtTagStart, end=self.re_gtTagEnd)
        self.re_gtTagStrDel = RegexGt(self.regexProperties.getRegex('stringDelimiter', self.re_gtTagStrDel.value()))
        self.re_gtTagParamDel = RegexGt(self.regexProperties.getRegex('paramDelimiter', self.re_gtTagParamDel.value()))
        self.re_gtTagParamAff = RegexGt(self.regexProperties.getRegex('paramAffectation', self.re_gtTagParamAff.value()))
        self.re_gtTagArOpen = RegexGt(self.regexProperties.getRegex('arrayOpen', self.re_gtTagArOpen.value()))
        self.re_gtTagArClose = RegexGt(self.regexProperties.getRegex('arrayClose', self.re_gtTagArClose.value()))
        self.re_gtTagTrans = RegexGt(self.regexProperties.getRegex('trans', self.re_gtTagTrans.value())).setDefaultTag(start=self.re_gtTagStart, end=self.re_gtTagEnd)
        self.re_gtTagParam = RegexGt(self.regexProperties.getRegex('param', self.re_gtTagParam.value())).setDefaultTag(start=self.re_gtTagStart, end=self.re_gtTagEnd)

        # Load messages from config file :
        self.re_mpTag = RegexGt(self.regexProperties.getRegex('messageTag', self.re_mpTag.value()))
        self.messageProperties = MessagesProperties(path=messagesPropertiesPath, language=language, regex=self.re_mpTag)
        if(None != messagesPropertiesPath):
            self.messageProperties.load()

    def translate(self, text):
        return self.re_gtTagTrans.compile().sub(self._replaceLabels, text)

    def _replaceLabels(self, matchobj):
        if(matchobj.group()=="" and len(matchobj.groupdict())<1):
            return ""
        elif(matchobj.group(2) != None):
            params = self.re_gtTagParam.findall(matchobj.group(2))
            paramsWithValues = {}
            for param in params:
                if(param):
                    paramsWithValues[param[0]] = self.re_gtTagParamValue.findall(param[1])
            return self.messageProperties.message(matchobj.group(1), parameters=paramsWithValues)
        else:
            return self.messageProperties.message(matchobj.group(1))

    def extractLabels(self, text):
        #print('Execute regexp : %s' % self.re_gtTagTrans.value())
        return self.re_gtTagTrans.findall(text)

    def extractLabelsParams(self, text):
        #print('Execute regexp : %s' % self.re_gtTagParam.value())
        return self.re_gtTagParam.findall(text)

