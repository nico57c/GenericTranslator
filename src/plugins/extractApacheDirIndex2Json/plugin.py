class Plugin(object):

    def run(self, output, parameters):
        output = output.replace('"',"'")
        lines = output.split('\n',)
        print('[')
        i = 0
        iPrec = i
        for line in lines:
            items = list(map(str.strip, line.split('--item--')))
            if(len(items)>2):
                if(iPrec<i):
                    print(',')
                    iPrec = i
                print('\t', end="")
                print({'filename': items[0].split('>')[1].split('</a')[0].strip(), 
                       'url': items[0].split('href=\'')[1].split('\'')[0].strip(), 
                       'date': items[1], 
                       'size': items[2]}, end="")
                i+=1
        print('\n]')