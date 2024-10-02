
from parser.common.spliter import split_groups
from parser.ja_general.pron_arch import create_ja_pron_arch


def parse_ja(wiki_cache_dir):
    # common operation for all languages, both ja and zh
    kanji_dict = split_groups(wiki_cache_dir)

    # common operation for ja, both onyomi and kunyomi
    pron_arch_dict = create_ja_pron_arch(kanji_dict)
    
    return pron_arch_dict