import sys
import os
from source.source import  get_source
from wiktionary.wikt import fetch_wikt
from wiktionary.check import check_wikt


if __name__ == '__main__':
    update_flag = False
    if len(sys.argv) == 2 and sys.argv[1] == 'update':
        update_flag = True
    kj_dict, kj_list = get_source()
    wiki_dict = fetch_wikt(kj_list, update_flag)
    check_wikt(wiki_dict)

