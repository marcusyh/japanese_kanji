import urllib3
import json
import traceback


#Wikimedia API Document location: https://en.wiktionary.org/w/api.php
#https://ja.wiktionary.org/w/api.php?action=parse&page=%E5%8F%B6&noimages=true&format=json&prop=sections
#https://ja.wiktionary.org/w/api.php?action=parse&page=%E5%8F%B6&noimages=true&format=json&prop=wikitext&section=4
#https://github.com/5j9/wikitextparser
#https://github.com/earwig/mwparserfromhell/

# A agent class which is used to map to remote wiktionary.org page to local object
class Agent():
    _url = 'https://%s.wiktionary.org/w/api.php'
    _fields = {'action': 'parse', 
            'page': '', 
            'format': 'json', 
            'prop': 'sections'}
    
    _ja_section_keywords = ['日本語', '中国語']   # ja.wiktionary.org
    _zh_section_parent_keywords = ['汉语', '漢語', '汉语族', '漢語族', '汉字', '漢字']   # zh.wiktionary.org
    _zh_section_keywords = ["發音", "发音", "讀音", "读音", "拼音"]

    def __init__(self):
        self.__http = urllib3.PoolManager()


    def _fetch_sections(self, kanji, lang):
        fields = {x: y for x, y in self._fields.items()}
        fields['page'] = kanji

        fetched_sections = []
        try:
            hdlr = self.__http.request('GET', self._url %lang, fields=fields)
            if hdlr.status != 200:
                raise Exception('Return value is not 200')
            fetched_sections = json.loads(hdlr.data.decode('utf-8'))['parse']['sections']
        except Exception:
            traceback.print_exc()
            fetched_sections = []
        
        # create a map for each section's anchor and it's index
        sections_map = [[item['anchor'], index] for index, item in enumerate(fetched_sections, start=1)]

        return sections_map


    def _fetch_pronunciation(self, kanji, index_lang, prop):
        index, lang = index_lang

        fields = {x: y for x, y in self._fields.items()}
        fields.update({
            'page': kanji,
            'prop': prop,
            'section': index
        })

        try:
            hdlr = self.__http.request('GET', self._url %lang, fields=fields)
            if hdlr.status != 200:
                raise Exception('Return value is not 200')
            return json.loads(hdlr.data.decode('utf-8'))['parse'][prop]['*']
        except Exception:
            traceback.print_exc()
            return ''


    def _get_ja_sections(self, kanji):
        sections_map = self._fetch_sections(kanji, 'ja')

        keywords_indices = []
        for keyword in self._ja_section_keywords:
            keyword_index= None
            for anchor, index in sections_map:
                if keyword == anchor:
                    keyword_index = index
                    break
            if keyword_index:
                keywords_indices.append([keyword_index, 'ja'])
            else:
                keywords_indices.append(None)
 
        return keywords_indices
    

    def _get_zh_sections(self, kanji):
        sections_map = self._fetch_sections(kanji, 'zh')

        keyword_indices = []
        found_parent = False
        for keyword in self._zh_section_parent_keywords:
            keyword_index = None
            for anchor, index in sections_map:
                if keyword == anchor:
                    found_parent = True
                if found_parent and anchor in self._zh_section_keywords:
                    keyword_index = index
                    break
            keyword_indices.append(keyword_index)
        
        for index in keyword_indices:
            if index != None:
                return [index, 'zh']
        return None


    def fetch(self, kanji, prop='wikitext'):
        indices_list = self._get_ja_sections(kanji)
        indices_list.append(self._get_zh_sections(kanji))
        if any([i == None for i in indices_list if i]):
            print(f'{kanji} has no pronunciation: {indices_list}')

        pronunciation_list = []
        for item in indices_list:
            if not item:
                pronunciation_list.append('')
                continue
            pronunciation_list.append(self._fetch_pronunciation(kanji, item, prop))
            
        return pronunciation_list

