import argparse
import os
from output import config
from wikt_parser import parse_ja_yomi
from output.kanji.wordslist_printer import output_wordslist
from output.kanji.wikt import convert_wikt_to_html


def add_wordslist_args(sub_parsers):
    wordslist_parser = sub_parsers.add_parser(
        'kanji',
        help='Process kanji data',
        description='Process and display kanji data with various options.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    wordslist_parser.add_argument(
        '-i', '--input_wiki_cache_dir',
        type=str,
        default=config.WIKT_CACHE_DIR,
        help='Path to the wiki cache. (default: ../data/wiktionary)'
    )
    wordslist_parser.add_argument(
        '-o', '--output_path',
        type=str,
        default=config.MARKDOWN_PATH,
        help=f'Dir to the output file containing wordslist data. If not specified, defaults to {config.MARKDOWN_PATH}.'
    )
    wordslist_parser.add_argument(
        '-w',
        '--wordslist',
        action='store_true',
        help='Generate kanji pronunciation and wordslist in json format',
    )
    wordslist_parser.add_argument(
        '-k',
        '--wiktionary',
        action='store_true',
        help='Generate kanji detail by wiktionary in html format',
    )

    
def genereate_kanji_detail(args):
    # Set default values if neither -l nor -k is specified
    if not args.wordslist and not args.wiktionary:
        args.wordslist = True
        args.wiktionary = True
    
    # generate wordslist
    if args.wordslist:
        # get kunyomi_dict
        kanji_yomi_dict, kanji_ydkey_map, all_kunyomi_keys = parse_ja_yomi(args.input_wiki_cache_dir)

        # output wordslist
        output_json_path = os.path.join(args.output_path, '日本語_単語.json')
        output_wordslist(output_json_path, kanji_yomi_dict, kanji_ydkey_map)
    
    # generate wiktionary detail
    if args.wiktionary:
        output_dir = os.path.join(args.output_path, 'wikt')
        convert_wikt_to_html(args.input_wiki_cache_dir, output_dir)

def regist_kanji_detail(sub_parsers):
    add_wordslist_args(sub_parsers)
    return {'kanji': genereate_kanji_detail}