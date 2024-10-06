import argparse
import os
from output import config
from wikt_parser import parse_ja_yomi
from output.wordslist_printer import output_wordslist


wordslist_file_path = os.path.join(config.MARKDOWN_PATH, f'{config.WORDS_FILENAME}.json')

def add_wordslist_args(sub_parsers):
    wordslist_parser = sub_parsers.add_parser(
        'wordslist',
        help='Process wordslist data',
        description='Process and display wordslist data with various options.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    wordslist_parser.add_argument(
        '-w', '--input_wiki_cache_dir',
        type=str,
        default=config.WIKT_CACHE_DIR,
        help='Path to the wiki cache. (default: ../data/wiktionary)'
    )
    wordslist_parser.add_argument(
        '-f', '--output_path',
        type=str,
        default=wordslist_file_path,
        help=f'Path to the output file containing wordslist data. If not specified, defaults to {wordslist_file_path}.'
    )

    
def genereate_wordslist(args):
    # get kunyomi_dict
    kanji_yomi_dict, kanji_ydkey_map, all_kunyomi_keys = parse_ja_yomi(args.input_wiki_cache_dir)
    
    # generate wordslist
    output_wordslist(args.output_path, kanji_yomi_dict, kanji_ydkey_map)


def regist_ja_wordslist(sub_parsers):
    add_wordslist_args(sub_parsers)
    return {'wordslist': genereate_wordslist}