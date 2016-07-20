
class Plugin(object):

    def run(self, output, parameters):
        res = 'detectedTag'
        for label in output:
            if(label[0] == "" and (res != 'detectedTag')):
                res = res[0:res.rfind('>')]
            if(label[1]=='"' or label[1]=="'"):
                res = res + '>' + label[0]
                print(res)
            else:
                print(res + '>' + label[0])