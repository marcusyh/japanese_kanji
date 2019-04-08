import sys
sys.path.insert(0, 'source')
from read_jouyou import read_jouyou
from read_jinmei import read_jinmei
from read_hougai import read_hougai
from read_itai import read_itai

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
    # kanji_dict used to save the respected result. 
    # The kanji which has the smallest unicode value of the itai kanji group will be treated as the key
    # All the kanji of the itai kanji group will be put in the value list
    kanji_dict = {}
    # Usded as an assistant dictionary
    # Any kanji appearred as the key, the key in kanji_dict as the value of them.
    temp_dict= {}

    def merge_to_sets(source, appendix):
        for ji, kana in source.items():
            if ji.strip().strip('/') == '':
                continue

            items = sorted(ji.split('/'))
            inside = [item for item in items if item in temp_dict]
            outside = list(set(items) - set(inside))
            
            # when inside list is empty, append all element in items list to kanji_dict with key items[0]
            if not inside:
                kanji_dict[items[0]] = {
                        'kanji': [appendix + item for item in items],
                        'kana': kana}
                temp_dict.update({item: items[0] for item in items})
                continue
            
            # when inside list is not emppty, and when items[0] is equal or bigger than the original key in kanji_dict, we still let the orignal key as the key
            if items[0] == temp_dict[inside[0]] or sorted([items[0], temp_dict[inside[0]]])[1] == items[0]:
                kanji_dict[temp_dict[inside[0]]]['kanji'] += [appendix + item for item in outside]
                kanji_dict[temp_dict[inside[0]]]['kana'].update(kana)
                temp_dict.update({item: temp_dict[inside[0]] for item in outside})
                continue
           
            # when inside list is not empty, and when items[0] is smaller than the orignal key, we replace the original key to items[0] 
            items2 = sorted(outside + [item[1] for item in kanji_dict[temp_dict[inside[0]]]['kanji']])
            kanji_dict[temp_dict[inside[0]]]['kanji'] += [appendix + item for item in outside]
            kanji_dict[temp_dict[inside[0]]]['kana'].update(kana)
            kanji_dict[items[0]] = kanji_dict[temp_dict[inside[0]]]
            del kanji_dict[temp_dict[inside[0]]]
            temp_dict.update({item: items[0] for item in items2})

    for source in args:
        merge_to_sets(source, str(args.index(source) + 1))

    return kanji_dict, list(temp_dict.keys())

def convert_to_writable(kanji_dict):
    writable = {}
    d = {'1': '', '2': '+', '3': '*', '4': '^'}
    h = open('/tmp/rslt.csv', 'w')
    for a, b in kanji_dict.items():
        key = '/'.join(list(map(lambda x: x[1] + d[x[0]], b['kanji'])))
        writable[key] = b['kana']
    return writable


def get_source():
    jouyou = read_jouyou()
    hougai = read_hougai()
    jinmei = read_jinmei()
    itai = read_itai()
    return merge_kanji(jouyou, hougai, jinmei, itai)

if __name__ == '__main__':
    from save_file import save_to_docx
    rslt = get_source()
    wrtb = convert_to_writable(rslt)
