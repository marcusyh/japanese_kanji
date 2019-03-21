from util_read import readfile

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

def read_hougai(appendix = ''):
    return deal_weblio(readfile('source/ひょうがいかんじじたいひょう'), appendix)


if __name__ == '__main__':
    hougai = read_hougai()
