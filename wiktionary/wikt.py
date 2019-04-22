import traceback
import os
from wiktionary.agent import Agent
from wiktionary.sections import check_wikitext, fetch_wikitext

CACHE = 'wiktionary/cache.txt'

def load_from_cache():
    if not os.path.isfile(CACHE):
        return {}
    wiki_dict = {}
    h = open(CACHE, 'r')
    for s in h.readlines():
        items = s.strip().replace('\\n', '\n').replace('\\r', '\r').split('\t')
        wiki_dict[items[0]] = '\t'.join(items[1:])
    h.close()
    return wiki_dict

def save_to_cache(wiki_dict):
    h = open(CACHE, 'w')
    for k, v in wiki_dict.items():
        s= '%s\t%s\n' %(k, v.replace('\n', '\\n').replace('\r', '\\r'))
        h.write(s)
    h.close()

def fetch_wiktdata(kanji_list, update_flag):
    wiki_dict = load_from_cache()
    if not update_flag:
        return wiki_dict

    agent = Agent()
    count = 0

    for kanji in kanji_list:
        if kanji in wiki_dict:
            continue
        continue

        try:
            index = agent.fectch_sections(kanji)
            if not index or int(index) > 99:
                print(kanji)
                continue

            wiki  = agent.fectch_youmi(kanji, index)
            if not wiki:
                print(kanji)
                continue

            wiki_dict[kanji] = wiki

        except Exception:
            traceback.print_exc()

        if count % 20 == 0:
            print(count)
        if count % 200 == 0 and count != 0:
            save_to_cache(wiki_dict)
            print('saved to cache')

        count += 1

    if count % 200 > 0:
        save_to_cache(wiki_dict)
    return wiki_dict 

def get_youmi(kj_list, update_flag):
    wiki_dict = fetch_wiktdata(kj_list, update_flag)
    if update_flag:
        check_wikitext(wiki_dict)
    return fetch_wikitext(wiki_dict)
    
if __name__ == '__main__':
    import sys
    from source.source import get_source
    update_flag = False
    if len(sys.argv) == 2 and sys.argv[1] == 'update':
        update_flag = True
    kj_dict, kj_list = get_source()
    wiki_text = get_youmi(kj_list, update_flag)

