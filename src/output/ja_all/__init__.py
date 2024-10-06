import os
from output import config
from wikt_parser import parse_ja_yomi
from output.wordslist_printer import output_wordslist
from output.ja_kunyomi import generate_kunyomi_file
from output.ja_onyomi import generate_onyomi_file



def output_ja_all(args):
    # get onyomi_dict
    kanji_yomi_dict, kanji_ydkey_map, all_onyomi_keys = parse_ja_yomi(args.input_wiki_cache_dir)
    
    # output kunyomi and onyomi
    generate_kunyomi_file(args, kanji_yomi_dict)
    generate_onyomi_file(args, kanji_yomi_dict)
    
    # output wordslist
    output_path = os.path.join(args.output_dir, f'{config.WORDS_FILENAME}.json')
    output_wordslist(output_path, kanji_yomi_dict, kanji_ydkey_map)
