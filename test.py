import sys
from source.source import  get_source
from wiktionary.wikt import get_youmi 


if __name__ == '__main__':
    update_flag = False
    if len(sys.argv) == 2 and sys.argv[1] == 'update':
        update_flag = True
    kj_dict, kj_list = get_source()
    wiki_text = get_youmi(kj_list, update_flag)

