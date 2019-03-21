from util_read import readfile

def deal_itai(source, appendix):
    kanji_set = {}
    
    for current in source:
        if current.strip() == '':
            continue
        items = current.strip().split(',')
        
        jis = []
        for ji in items:
            if not ji.strip():
                continue
            jis.append(ji.strip() + appendix)

        kanji_set['/'.join(jis)] = {}

    return kanji_set

def read_itai(appendix = ''):
    return deal_itai(readfile('source/いたいじ'), appendix)


if __name__ == '__main__':
    itai = read_itai()
