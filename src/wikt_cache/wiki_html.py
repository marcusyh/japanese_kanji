import os
import json
from wikt_cache.remote_agent import Agent
from wikt_cache.wiki_cache import WikiCache
from file_util import prepare_file_path

def _get_kanji_list(cache_dir):
    wiki_cache = WikiCache(cache_dir)
    kanji_list1 = wiki_cache.wiki_dict.keys()
    kanji_list2 = wiki_cache.patch.keys()
    return list(set(kanji_list1).union(set(kanji_list2)))
 

def _save_html(html_path, kanji, html_list):
    ja_html, zh_html1, zh_html2 = html_list
    html_dict = {
        "ja": ja_html,
        "zh1": zh_html1,
        "zh2": zh_html2,
    }
    file_path = os.path.join(html_path, f'{kanji}.json')
    with open(file_path, 'w') as file:
        json.dump(html_dict, file, ensure_ascii=False)


def fetch(kanji_list, html_path):
    agent = Agent()
    for count, kanji in enumerate(kanji_list):
        ja_text, zh_text1, zh_text2 = agent.fetch(kanji, prop='text')
        _save_html(html_path, kanji, [ja_text, zh_text1, zh_text2])
        if count % 10 == 0:
            print(f'{count} fetched.')


def fetch_wiki_html(cache_path, update_flag=True, fetch_missing_only=False):
    html_path = os.path.join(cache_path, 'html')
    prepare_file_path(html_path, is_dir=True, create_if_not_exists=True, delete_if_exists=False)

    kanji_list = _get_kanji_list(cache_path)
    
    fetch(kanji_list, html_path)
