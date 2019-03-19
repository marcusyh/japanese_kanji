from source.read_jouyou import read_jouyou
from source.read_jinmei import read_jinmei
from source.read_hougai import read_hougai
from source.read_itai import read_itai


def merge_kanji():
    jouyou = read_jouyou()
    jinmei = read_jinmei()
    hougai = read_hougai()
    itai = read_itai()

    kanji_sets = {}
    
    for ji in youyou.keys():
        items = sorted(ji.split('/'))
        if items[0] not in kanji_sets:
            kanji_sets[items[0]] = {}
        kanji_sets[items[0]] = 
        
from classify_data import get_classified
from classify_data import add_alter
from save_file import save_to_docx
from save_file import save_to_csv


FILENAME = '常用汉字列表音読み'
FILEPATH = '/mnt/c/Users/cj/Desktop'


if __name__ == '__main__':
    hira, kata = get_classified(jouyou, jinmei, hougai)
    kata, remains = add_alter(kata)

    save_to_docx(kata, FILENAME, FILEPATH)
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
    a = {'a1': {'a11': 'a111', 'a12': 'a121'}, 'a1': {'a11': 'a111', 'a12': 'a121'}}
    b = {'b1': {'b11': 'b111', 'b12': 'b121'}, 'b1': {'b11': 'b111', 'b12': 'b121'}}
    c = {'c1': {'c11': 'c111', 'c12': 'c121'}, 'c1': {'c11': 'c111', 'c12': 'c121'}, '': {}}
    x, y = get_classified(a, b, c)
