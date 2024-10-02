import json
import shutil
import os
from wiktionary.remote_agent import Agent

class WikiCache:
    """
    A caching system for storing and retrieving parsed Wiktionary data about Japanese kanji characters.

    Attributes:
        cache_path (str): Path to the text file used for caching the wiktionary data.
        wiki_dict (dict): Dictionary to store kanji and their associated data from Wiktionary.
        agent (Agent): An instance of Agent class for fetching data from Wiktionary API.

    Methods:
        __init__: Constructor to initialize the WikiCache instance and load existing cached data.
        _create_agent: Initializes and returns an Agent if not already done.
        _load: Loads the cache from a file specified by `cache_path` into `wiki_dict`.
        _save: Saves the current data from `wiki_dict` to a file specified by `cache_path`.
        update: Refreshes the cached data for the existing kanji entries in `wiki
        fetch: Fetches the data for a list of kanji characters using the Agent and updates the cache.
    """
    def __init__(self, cache_path):
        self.cache_path = cache_path
        self.agent = None
        self.wiki_dict = self._load()


    def _create_agent(self):
        if not self.agent:
            self.agent = Agent()
        return self.agent


    def _load(self):
        if not os.path.isfile(self.cache_path):
            return {}
        wiki_dict = {}
        with open(self.cache_path, 'r') as file:
            for line in file:
                key, *values = line.strip().replace('\\n', '\n').replace('\\r', '\r').split('\t')
                if key in self.patch:
                    continue
                wiki_dict[key] = values
        return wiki_dict


    def _save(self):
        shutil.copy(self.cache_path, self.cache_path + '.bak')
        with open(self.cache_path, 'w') as file:
            for k, v in self.wiki_dict.items():
                v = [x.replace('\t', '') for x in v]
                s = '\t'.join([k] + v) + '\n'
                s = s.replace('\n', '\\n').replace('\r', '\\r')
                file.write(s+'\n')
        print('saved to cache')


    def update(self):
        self.fetch(list(self.wiki_dict.keys()))


    def fetch(self, kanji_list):
        agent = self._create_agent()
        for count, kanji in enumerate(kanji_list):
            ja_text, zh_text1, zh_text2 = agent.fetch(kanji)
            self.wiki_dict[kanji] = [ja_text, zh_text1, zh_text2]
            if count % 10 == 0:
                print(f'{count} fetched.')
        self._save()
        

    def cache_info(self):
        if not os.path.isfile(self.cache_path):
            return None

        kanji_list = []
        with open(self.cache_path, 'r') as file:
            for line in file:
                kanji = line.split('\t')[0]
                kanji_list.append(kanji)
                
        file_info = os.stat(self.cache_path)
        return {
            'kanji_count': len(kanji_list),
            'kanji_list': kanji_list,
            'file_size': file_info.st_size,
            'update_time': file_info.st_mtime
        }
