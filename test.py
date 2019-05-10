import sys
from source.source import  get_source
from wiktionary.wikt import get_youmi 


if __name__ == '__main__':
    update_flag = False
    if len(sys.argv) == 2 and sys.argv[1] == 'update':
        update_flag = True
    kj_dict, kj_list = get_source()
    wiki_text = get_youmi(kj_list, update_flag)

    def get_star_number(string): 
        count = 0
        while string.startswith('*'):
            string = string[1:]
            count += 1
        return count
    
    ydict = {}
    import re
    h1 = open('/tmp/youmi.txt', 'w')
    h2 = open('/tmp/youmi2.txt', 'w')
    for k, v in wiki_text.items():
        s = v.string.replace('\n', '\\n')
                #'(?P<name2>[^=><!]*(?:<!--[^<!>]*-->)?[^=><!]*(?:<!--[^<!>]*-->)?)' \
        x = re.match(\
                '(?P<name0> *(={2,5}[^=]*={2,5})* *(\\\\n)* *(={2,5}[^=]*={2,5})* *(<!--[^<!>]*-->)? *(\\\\n)*)? *' \
                '(?P<name1>([^=><!]*(<[^<!>]*>)?[^=><!]*)*)' \
                '(?P<name2><!--[^<!>]*-->)*' \
                '(?P<name3> *={2,4}\{\{[^=]*\}\}={2,4} *)?' \
                '(?P<name4>.*)?' \
                     , s)
        if not x:
            print(k, v)
            continue
        y = x.groupdict()
        z = k + '\t' + '\t'.join([str(y[k]) for k in sorted(y)]) + '\n'
        h1.write('%s\t%s\n' %(k, y['name1']))
        h2.write(z)
        youmi = y['name1'].split('\n')
        ydict[k] = {}
        for i in youmi:
            line = i.strip()
            if not line:
                continue
            if not line.startswith('*'):
                print(k, y['name1'], line)
            while string.startswith('*'):
                string = string[1:]
                ydict[k][
            ydict[k][line] = {}
        x = re.match( \
                , youmi)
        #if y['name5'] and y['name5'].find('*') >= 0:
        #    z = '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(k, y['name0'], y['name1'], y['name2'], y['name3'], y['name4'], y['name5'])
        #    print(z)
    h1.close()
    h2.close()
        #print(z)
