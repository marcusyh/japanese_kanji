from file_util import prepare_directory
from preparation.loader import load_local_kanji_without_tag
from wiktionary.wiki_cache import WikiCache
from wiktionary.ui import confirm_fetch_remote, show_kanji_list, show_brief_info


def get_kanji_list(source_data_dir):
    kanji_dict = load_local_kanji_without_tag(source_data_dir)
    kanji_list = set()
    for key, value in kanji_dict.items():
        key = key.strip()
        if not key:
            continue
        kanji_list.add(key)
        kanji_list.update([kanji for kanji in value if kanji.strip()])
    return set(kanji_list)


def fetch_wikt_cache(source_data_dir, cache_path, update_flag=False, fetch_missing_only=True):
    prepare_directory(cache_path)

    wc = WikiCache(cache_path)
    cache_info = wc.cache_info()
    local_kanji_set = get_kanji_list(source_data_dir)

    if cache_info is None or not cache_info['kanji_count']:
        cache_kanji_set = set()
    else:
        cache_kanji_set = set(kanji for kanji in cache_info['kanji_list'] if kanji.strip())
    missing_kanji_set = local_kanji_set - cache_kanji_set
    update_kanji_set = cache_kanji_set - missing_kanji_set
    
    show_brief_info(len(local_kanji_set), len(cache_kanji_set), len(missing_kanji_set), fetch_missing_only)
    show_kanji_list(missing_kanji_set, update_kanji_set, fetch_missing_only)
    confirm_fetch_remote()
         
    if update_flag:
        wc.fetch(list(update_kanji_set.union(missing_kanji_set)))
    else:
        wc.fetch(list(missing_kanji_set))