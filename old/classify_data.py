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

def add_alter(sets):
    tmp = {}
    for i, a in sets.items():
        for j in a.keys():
            if j not in tmp:
                tmp[j] = []
            tmp[j].append(i)
    multi = {x: y for x, y in tmp.items() if len(y) >= 2}
    
    # For kanji which has one sound, or which share sound with other kanji
    newsets = {}
    # For kanji which has 2 ore more sounds and do not share any sound with other kanji
    remains = {}
    multi_saver = {}
    for i, a in sets.items():

        tmp = {}
        for j, k in a.items():
            if j not in multi:
                continue
            for p in multi[j]:
                if p == i:
                    continue
                z = '/'.join(sorted([i,p]))
                tmp[z] = tmp.get(z, [])
                tmp[z].append(j)
            if z in multi_saver and multi_saver[z] != tmp[z]:
                print(multi_saver[z], tmp[z])
            else:
                multi_saver[z] = tmp[z]
        tmp_sounds = []
        tmp_kanji = []
        for x, y in tmp.items():
            if len(y) <= 1:
                continue
            tmp_sounds += x.split('/')
            tmp_kanji += y
            newsets[x] = newsets.get(x, {})
            for j in y:
                newsets[x][j] = a[j]

        for j, k in a.items():
            if j in tmp_kanji:
                continue
            # For kanji which has one sound, or which share sound with other kanji
            l = '%s(%s)' %(j, '/'.join([x for x in multi[j] if i != x])) if j in multi else j
            newsets[i] = newsets.get(i, {})
            newsets[i][l] = k

            # For kanji which has 2 or more sounds and do not share any sound with other kanji
            if j in multi:
                if j not in remains:
                    remains[j] = {}
                remains[j][i] = k

    return newsets, remains

if __name__ == '__main__':
    a = {'a1': {'a11': 'a111', 'a12': 'a121'}, 'a1': {'a11': 'a111', 'a12': 'a121'}}
    b = {'b1': {'b11': 'b111', 'b12': 'b121'}, 'b1': {'b11': 'b111', 'b12': 'b121'}}
    c = {'c1': {'c11': 'c111', 'c12': 'c121'}, 'c1': {'c11': 'c111', 'c12': 'c121'}, '': {}}
    x, y = get_classified(a, b, c)
