from source.read_jouyou import read_jouyou
from source.read_jinmei import read_jinmei
from source.read_hougai import read_hougai
from source.read_itai import read_itai
from save_file import save_to_docx


def _reorgnize(*args):
    new_kanjiset = {}
    for kanji_set in args:
        for a, y in kanji_set.items():
            for b, c in y.items():
                if b not in new_kanjiset:
                    new_kanjiset[b] = {}
                new_kanjiset[b][a] = c
    return new_kanjiset

def _check_katakana_hirakana(word):
    all_hira = True
    all_kata = True
    for i in word:
        all_hira = all_hira and u'\u3040' <= i <= u'\u309F'
        all_kata = all_kata and u'\u30A0' <= i <= u'\u30FF'
    return all_hira, all_kata

def _get_result(kanji):
    hira_set = {}
    kata_set = {}
    pointer = None
    for x, y in kanji.items():
        hira, kata = _check_katakana_hirakana(x)
        if hira and kata or not hira and not kata:
            print(x, y)
            continue
        pointer = hira_set if hira else kata_set
        pointer[x] = y
    return hira_set, kata_set


def get_classified(*args):
    return _get_result(_reorgnize(*args))

if __name__ == '__main__':
    jouyou = read_jouyou()
    hougai = read_hougai()
    jinmei = read_jinmei()
    itai = read_itai()

    rslt = merge_kanji(jouyou, hougai, jinmei, itai)
    wrtb = convert_to_writable(rslt)
    
