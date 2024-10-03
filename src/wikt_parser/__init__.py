
from wikt_cache.wiki_cache import WikiCache
from wikt_parser.wiktext_spliter import split_groups
from wikt_parser.ja_parser import create_ja_pron_arch
from wikt_parser.ja_onyomi_parser import parse_onyomi


def parse_ja_onyomi(wiki_cache_dir):
    wiki_cache = WikiCache(wiki_cache_dir)

    # common operation for all languages, both ja and zh
    kanji_dict = split_groups(wiki_cache.wiki_dict)

    # common operation for ja, both onyomi and kunyomi
    pron_arch_dict = create_ja_pron_arch(kanji_dict)
    
    # parse onyomi and kunyomi
    onyomi_dict, all_onyomi_keys = parse_onyomi(pron_arch_dict)
    
    return onyomi_dict, all_onyomi_keys
