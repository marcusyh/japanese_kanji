
from wikt_cache.wiki_cache import WikiCache
from wikt_parser.wiktext_spliter import split_groups
from wikt_parser.ja_parser import create_ja_pron_arch
from wikt_parser.ja_onyomi_parser import parse_onyomi
from wikt_parser.wikt_bugfix import fix_by_wikt_patch, merge_with_preparation


def parse_ja_onyomi(wiki_cache_dir):
    wiki_cache = WikiCache(wiki_cache_dir)

    # common operation for all languages, both ja and zh
    kanji_dict = split_groups(wiki_cache.wiki_dict)

    # common operation for ja, both onyomi and kunyomi
    pron_arch_dict = create_ja_pron_arch(kanji_dict)
    
    # parse onyomi and kunyomi
    wikt_onyomi_dict, wikt_all_onyomi_keys = parse_onyomi(pron_arch_dict)
    
    # fix wikt data by patch
    fix_by_wikt_patch(wikt_onyomi_dict)
    
    # merge wikt data by patch
    merged_wikt_onyomi_dict = merge_with_preparation(wikt_onyomi_dict)
    
    return merged_wikt_onyomi_dict, wikt_all_onyomi_keys


        