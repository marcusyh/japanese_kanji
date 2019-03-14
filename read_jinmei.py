import urllib3
import json
import traceback
import re
from util_read import readfile

#https://ja.wiktionary.org/w/api.php?action=parse&page=%E5%8F%B6&noimages=true&format=json&prop=sections
#https://ja.wiktionary.org/w/api.php?action=parse&page=%E5%8F%B6&noimages=true&format=json&prop=wikitext&section=4

class Jinmei():
    _url = 'https://ja.wiktionary.org/w/api.php'
    _fields = {'action': 'parse', 
            'page': '', 
            'noimages': True, 
            'format': 'json', 
            'prop': 'sections'}

    def __init__(self):
        self.__http = urllib3.PoolManager()

    def __fectch_sections(self, kanji):
        try:
            fields = {x: y for x, y in self._fields.values()}
            fields['page'] = kanji
            hdlr = self.__http.request('GET', fields=fields)
            if hdlr.status != 200:
                raise Exception('Return value is not 200')
            rslt = json.loads(hdlr.data.decode('utf-8'))['parse']['sections']
            index = 0
            for item in rslt:
                if item['anchor'] == '発音':
                    return index
                index += 1
        except Exception:
            traceback.print_exc()

    def __fectch_youmi(self, kanji, index):
        fields = {x: y for x, y in self._fields.values()}
        fields.update({'page': kanji, 'prop': 'wikitext', section: index})
        try:
            hdlr = self.__http.request('GET', fields=fields)
            rslt = json.loads(hdlr.data.decode('utf-8'))['parse']['wikitext']
            index = 0
            for item in rslt:
                if item['anchor'] == '発音':
                    return index
                index += 1
        except Exception:
            traceback.print_exc()

    def fetch_section(kanji):
        hdlr = urllib3.Pool
    
    def read_jinmei():
        return deal_joyokanji(readfile('じんめいじょうようかんじひょう'), '*')
    
if __name__ == '__main__':
    jinmei = read_jinmei()
