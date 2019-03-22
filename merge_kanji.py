from source.read_jouyou import read_jouyou
from source.read_jinmei import read_jinmei
from source.read_hougai import read_hougai
from source.read_itai import read_itai

def merge_kanji_without_tag(jouyou, hougai, jinmai, itai):
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

def merge_kanji(*args):
    kanji_dict = {}
    temp_dict= {}

    def merge_to_sets(source, appendix):
        for ji in source.keys():
            if ji.strip().strip('/') == 0:
                continue

            items = sorted(ji.split('/'))
            inside = [item for item in items if item in temp_dict]
            outside = list(set(items) - set(inside))

            if not inside:
                kanji_dict[items[0]] = [appendix + item for item in items]
                temp_dict.update({item: items[0] for item in items})
                continue

            if inside[0] == temp_dict[inside[0]]:
                kanji_dict[items[0]] += [appendix + item for item in outside]
                temp_dict.update({item: items[0] for item in outside})
                continue
            
            items2 = sorted(kanji_dict[temp_dict[inside[0]]] + outside) 
            kanji_dict[items2[0]] = [appendix + item for item in items2]
            print(inside[0], kanji_dict[inside[0]])
            del kanji_dict[temp_dict[inside[0]]]
            temp_dict.update({item: items2[0] for item in items2})

    for source in args:
        merge_to_sets(source, args.index(source) + 1)

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

    rslt = merge_kanji(jouyou, hougai, jinmei, itai)
