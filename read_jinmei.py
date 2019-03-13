import urllib3
from util_read import readfile

#https://ja.wiktionary.org/w/api.php?action=parse&page=%E5%8F%B6&noimages=true&format=json&prop=sections
#https://ja.wiktionary.org/w/api.php?action=parse&page=%E5%8F%B6&noimages=true&format=json&prop=wikitext&section=4

class Jinmei():
    _url = 'https://ja.wiktionary.org/w/api.php'
    _fields = {'action': 'parse', 
            'page': '叶', 
            'noimages': True, 
            'format': 'json', 
            'prop': 'sections'}

    def __init__(self):
        self.__http = urllib3.PoolManager()

    def __fectch_sections(self, kanji):
        fields = {x: y for x, y in self._fields.values()}
        fields['page'] = kanji
        hdlr = self.__http.request('GET', fields=fields)

    def __fectch_youmi(self, kanji, index):
        fields = {x: y for x, y in self._fields.values()}
        fields['page'] = kanji
        fields['prop'] = 'wikitext'
        fields['section'] = index
        hdlr = self.__http.request('GET', fields=fields)


    def fetch_section(kanji):
        hdlr = urllib3.Pool
    
    def read_jinmei():
        return deal_joyokanji(readfile('じんめいじょうようかんじひょう'), '*')
    
if __name__ == '__main__':
    jinmei = read_jinmei()
