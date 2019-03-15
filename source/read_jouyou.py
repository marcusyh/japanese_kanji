from util_read import readfile

def deal_joyokanji(source, appendix):
    kanji_set = {}
    previous = '*'
    
    ji = []
    ji_flag = True
    yomi = {}

    source.append('*')
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
            previous = current
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


def read_jouyou():
    return deal_joyokanji(readfile('じょうようかんじひょう'), '')

if __name__ == '__main__':
    jouyou = read_jouyou()
