from file_util import prepare_directory
from preparation.loader import load_local_kanji_without_tag
from wiktionary.wiki_cache import WikiCache
from wiktionary.ui import confirm_fetch_list, confirm_fetch_remote


def get_kanji_list(source_data_dir):
    kanji_dict = load_local_kanji_without_tag(source_data_dir)
    kanji_list = set()
    for key, value in kanji_dict.items():
        kanji_list.add(key)
        kanji_list.update(value)
    return kanji_list


def fetch_wikt_cache(source_data_dir, cache_path, update_flag=False, fetch_missing_only=True):
    prepare_directory(cache_path)

    wc = WikiCache(cache_path)
    cache_info = wc.cache_info()
    kanji_list = get_kanji_list(source_data_dir)

    if cache_info is None or not cache_info['kanji_count']:
        current_cache_list = []
    else:
        current_cache_list = cache_info['kanji_list']
         
    if not update_flag:
        fetch_list = confirm_fetch_list(current_cache_list, kanji_list, fetch_missing_only)
        confirm_fetch_remote(fetch_list)
        wc.fetch(fetch_list)
    else:
        confirm_fetch_remote(fetch_list)
        wc.update()