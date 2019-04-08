import traceback
from wiktionary.agent import Agent

CACHE = 'wiktionary/cache.txt'

def load_from_cache():
    wiki_dict = {}
    h = open(CACHE, 'r')
    for s in h.readlines():
        items = s.strip().split('\t')
        wiki_dict[items[0]] = '\t'.join(items[1:])
    h.close()
    return wiki_dict

def save_to_cache(wiki_dict):
    h = open(CACHE, 'w')
    for k, v in wiki_dict.items():
        s= '%s\t%s\n' %(k, v.replace('\n', ' ').replace('\r', ' '))
        h.write(s)
    h.close()

def fetch_wikt(kanji_list):
    wyoumi = Agent()
    wiki_dict = load_from_cache()
    count = 0

    for kanji in kanji_list:
        if kanji in wiki_dict:
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
        count += 1

    save_to_cache(wiki_dict)
    return wiki_dict 

if __name__ == '__main__':
    from source.source import get_source
    kj_list = list(get_source().keys())
    wiki_dict = fetch_wikt(kj_list)

