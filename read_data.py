import os

def readfile(dirname):
    data = []
    for f in os.listdir(dirname):
        fpath = os.path.join(dirname, f)
        h = open(fpath, 'r')
        for i in h.readlines():
            if i.strip() == '':
                continue
            data.append(i.strip())
        h.close()
    return data


def deal_joyokanji(source, appendix):
    kanji_set = {}
    previous = '*'
    
    ji = []
    ji_flag = True
    yomi = {}
    for current in source:
        if current == '' or current == '*' and previous == '*':
            continue

        if current == '*':
            previous = current
            kanji_set['/'.join(ji)] = yomi
            ji = []
            ji_flag = True
            yomi = {}
            continue

        ji_flag = len(current) == 1 and ji_flag
        if ji_flag:
            ji.append(current + appendix)
            continue

        items = [x.strip() for x in current.split('\t')]
        if len(items) > 3:
            print(items)
        elif len(items) == 3 and len(ji) == 0 and len(items[0]) == 1:
            ji.append(items[0] + appendix)
            yomi[items[1]] = items[2]
        elif len(items) == 3:
            print(items)
        elif len(items) == 2:
            yomi[items[0]] = items[1]
        else:
            yomi[items[0]] = ''
        previous = current

    return kanji_set


def deal_weblio(source, appendix):
    kanji_set = {}
    
    for current in source:
        if current == '':
            continue
        items = current.split(',')
        sound = items[0].strip()
        
        jis = []
        for ji in items[1:]:
            if not ji.strip():
                continue
            jis.append(ji.strip() + appendix)

        kanji_set['/'.join(jis)] = {sound: ''}

    return kanji_set


def read_jouyou():
    return deal_joyokanji(readfile('じょうようかんじひょう'), '')

def read_jinmei():
    return deal_joyokanji(readfile('じんめいじょうようかんじひょう'), '*')

def read_hougai():
    return deal_weblio(readfile('ひょうがいかんじじたいひょう'), '+')


if __name__ == '__main__':
    jouyou = read_jouyou()
    jinmei = read_jinmei()
    hougai = read_hougai()
