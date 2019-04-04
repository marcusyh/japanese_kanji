import traceback
from source.source import get_source
from wiki_youmi import WikiYoumi

def load_from_cache():
    wiki_dict = {}
    h = open('wiki_cache.txt', 'r')
    for s in h.readlines():
        items = s.strip().split('\t')
        wiki_dict[items[0]] = '\t'.join(items[1:])
    h.close()
    return wiki_dict

def save_to_cache(wiki_dict):
    h = open('wiki_cache.txt', 'w')
    for k, v in wiki_dict.items():
        s= '%s\t%s\n' %(k, v.replace('\n', ' ').replace('\r', ' '))
        h.write(s)
    h.close()

def fetch_remote(source):
    wyoumi = WikiYoumi()
    wiki_dict = load_from_cache()
    count = 0

    for kanji, v in source.items():
        if count % 1 == 0:
            print(count)

        count += 1
        if kanji in wiki_dict:
            print(kanji, 'in cache')
            continue

        try:
            for key in [kanji] + [x[1] for x in v['kanji'] if x != kanji]:
                index = wyoumi.fectch_sections(kanji)
                if index and int(index) <= 99:
                    break
            if not index or int(index) > 99:
                print(kanji)
                continue

            wiki  = wyoumi.fectch_youmi(kanji, index)
            if not wiki:
                print(kanji)
                break
            wiki_dict[kanji] = wiki

        except Exception:
            traceback.print_exc()

        if count % 200 == 0 and count != 0:
            save_to_cache(wiki_dict)
            print('saved to cache')

    save_to_cache(wiki_dict)
    return wiki_dict 

if __name__ == '__main__':
    source = get_source()
    wiki_dict = fetch_remote(source)

