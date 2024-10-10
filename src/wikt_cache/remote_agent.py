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
    _section_keywords_group = {
        'ja': [
            ['日本語'],
            ['中国語']
        ],
        'zh': [
            ['汉语', '漢語', '汉语族', '漢語族', '汉字', '漢字']
        ]
    }

    def __init__(self):
        self.__http = urllib3.PoolManager()

    def _fetch_sections(self, fields, lang):
        try:
            hdlr = self.__http.request('GET', self._url %lang, fields=fields)
            if hdlr.status != 200:
                raise Exception('Return value is not 200')
            return json.loads(hdlr.data.decode('utf-8'))['parse']['sections']
        except Exception:
            traceback.print_exc()
            return []


    def fetch(self, kanji, prop='wikitext'):
        """
        Fetches the text related to specified sections from the Japanese Wiktionary page for a given kanji character.

        Parameters:
            kanji (str): The kanji character whose Wiktionary data is to be fetched.
        
        Returns:
            list: A list of text contents from the specified sections. If a section is not found, an empty string is added for that section.

        Description:
            This method utilizes the Wiktionary API to retrieve information about certain sections relevant to the input kanji.
            It begins by configuring API fields using predefined values which specify the action, formatting, and properties that dictate the nature of the API request.
            The method fetches the available sections for the kanji from Wiktionary, searching for sections whose keywords match predefined groups.
            If a matching section is found, its textual content is fetched using the "wikitext" property, otherwise an empty string is added for that keyword group.
            Sections are identified by keywords like '発音' (pronunciation) among others. The method handles the HTTP request, error checking, and parsing of the JSON response.
        """
        text_list = []

        for lang, section_keywords_group in self._section_keywords_group.items():
            # init the query fiels
            fields = {x: y for x, y in self._fields.items()}
            fields['page'] = kanji

            # fetch sections summary info
            sections = self._fetch_sections(fields, lang)

            # create a map for each section's anchor and it's index
            sections_map = {item['anchor']: index for index, item in enumerate(sections, start=1)}

            for keywords_list in section_keywords_group:
                # get index of section for this keywords_list
                keywords_index = None
                for keyword in keywords_list:
                    if keyword in sections_map:
                        keywords_index = sections_map[keyword]
                        break
                
                # there is no content in wikitionary page for current keywords_list of this kanji
                if not keywords_index:
                    text_list.append('')
                    print(f'{kanji}, {lang}, {keywords_list}, section empty')
                    continue
                
                # update fields to prepare the query
                fields.update({'prop': prop, 'section': keywords_index})

                # fetch the pronunciation of the kanji
                try:
                    hdlr = self.__http.request('GET', self._url %lang, fields=fields)
                    wikitext = json.loads(hdlr.data.decode('utf-8'))['parse'][prop]['*']
                    text_list.append(wikitext)
                except Exception:
                    traceback.print_exc()
                    print(f'{kanji}, {lang}, {keywords_list}, index empty')
                    text_list.append('')

        return text_list