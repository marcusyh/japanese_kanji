import urllib3
import json
import traceback
import re

#https://ja.wiktionary.org/w/api.php?action=parse&page=%E5%8F%B6&noimages=true&format=json&prop=sections
#https://ja.wiktionary.org/w/api.php?action=parse&page=%E5%8F%B6&noimages=true&format=json&prop=wikitext&section=4
#https://github.com/5j9/wikitextparser
#https://github.com/earwig/mwparserfromhell/

class Agent():
    _url = 'https://ja.wiktionary.org/w/api.php'
    _fields = {'action': 'parse', 
            'page': '', 
            'noimages': True, 
            'format': 'json', 
            'prop': 'sections'}

    def __init__(self):
        self.__http = urllib3.PoolManager()

    def fectch_sections(self, kanji):
        try:
            fields = {x: y for x, y in self._fields.items()}
            fields['page'] = kanji
            hdlr = self.__http.request('GET', self._url, fields=fields)
            if hdlr.status != 200:
                raise Exception('Return value is not 200')
            rslt = json.loads(hdlr.data.decode('utf-8'))['parse']['sections']
            index = 0
            for item in rslt:
                if item['anchor'] == '発音':
                    return index
                if item['anchor'] == '読み':
                    return index
                index += 1
        except Exception:
            traceback.print_exc()
            return 9999

    def fectch_youmi(self, kanji, index):
        fields = {x: y for x, y in self._fields.items()}
        fields.update({'page': kanji, 'prop': 'wikitext', 'section': index})
        try:
            hdlr = self.__http.request('GET', self._url, fields=fields)
            rslt = json.loads(hdlr.data.decode('utf-8'))['parse']['wikitext']['*']
            return rslt
        except Exception:
            traceback.print_exc()

if __name__ == '__main__':
    wa = Agent()
