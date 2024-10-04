def _reorgnize(*args):
    new_kanjiset = {}
    for kanji_set in args:
        for a, y in kanji_set.items():
            for b, c in y.items():
                if b not in new_kanjiset:
                    new_kanjiset[b] = {}
                new_kanjiset[b][a] = c
    return new_kanjiset

def check_katakana_hirakana(word):
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
        hira, kata = check_katakana_hirakana(x)
        if hira and kata or not hira and not kata:
            print(x, y)
            continue
        pointer = hira_set if hira else kata_set
        pointer[x] = y
    return hira_set, kata_set


def get_classified(*args):
    return _get_result(_reorgnize(*args))