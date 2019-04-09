from source.source import  get_source
from wiktionary.wikt import fetch_wikt


if __name__ == '__main__':
    kj_dict, kj_list = get_source()
    wiki_dict = fetch_wikt(kj_list)

