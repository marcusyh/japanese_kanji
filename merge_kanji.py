from source.read_jouyou import read_jouyou
from source.read_jinmei import read_jinmei
from source.read_hougai import read_hougai
from source.read_itai import read_itai

def merge_kanji(jouyou, hougai, jinmai, itai):
    kanji_dict = {}
    
    for ji in list(jouyou.keys()) + list(jinmei.keys()) + list(hougai.keys()) + list(itai.keys()):
        items = sorted(ji.split('/'))
        print(ji)
        if len(items) < 1:
            continue
        for item in items:
            if item in kanji_dict:
                break 
        kanji_dict[items[0]] = set.union(kanji_dict.get(item, set()), set(items))
        if items.index(item) != 0 and item in kanji_dict:
            del kanji_dict[item]

    return kanji_dict

def merge_kanji_with_tag(jouyou, hougai, jinmei, itai):
    kanji_dict = {}
    tmp_dict= {}

    def merge_to_sets(source, appendix):
        for ji in source.keys():
            if ji.strip().strip('/') == 0:
                continue

            sorted(ji.split('/'))
            inside = [item for item in items if item in temp_dict]
            outside = list(sets(items) - sets(inside))

            if not inside:
                kanji_dict[items[0]] = [item + appendix for item in items]
                tmp_dict.update({item: items[0] for item in items})
                continue

            if inside[0] == items[0]:
                kanji_dict[items[0]].append([item + appendix for item in outside])
                tmp_dict.update({item: items[0] for item in outside})
                continue

            kanji_dict[items[0]] = kanji_dict[inside[0]] + [item + appendix for item in outside]
            del kanji_dict[inside[0]]
            tmp_dict.update({item: items[0] for item in items})

    merge_to_sets(jouyou, '1')
    merge_to_sets(hougai, '2')
    merge_to_sets(jinmei, '3')
    merge_to_sets(igai, '4')

    return kanji_dict

       
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

    rslt = merge_kanji2(jouyou, hougai, jinmei, itai)
