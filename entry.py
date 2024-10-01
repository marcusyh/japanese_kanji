from kanji_local import load_local_kanji
from wiktionary.cache import WikiCache
from wiktionary.ja import parsing_ja

if __name__ == '__main__':
    #kanji_result, kanji_list = load_local_kanji()
    #print("Total kanji:", len(kanji_list))

    #wc = WikiCache()
    #wc.fetch(kanji_list)

    parsing_ja()
