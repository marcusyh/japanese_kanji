import argparse
import os
import config
from wikt_parser import parse_ja_yomi
from output.kanji.wordslist_printer import output_wordslist
from output.kanji.wiktionary import convert_wikt_to_html

wordslist_path = os.path.join(config.OUTPUT_ROOT, f'{config.WORDS_FILENAME}.json')

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
    wordslist_parser.add_argument(
        '-ow', '--wordslist_output_path',
        type=str,
        default=wordslist_path,
        help=f'Dir to the wordslist output file. If not specified, defaults to {wordslist_path}.'
    )
    wordslist_parser.add_argument(
        '-ok', '--html_output_path',
        type=str,
        default=config.HTML_PATH,
        help=f'Dir to the wiktionary output file. If not specified, defaults to {config.HTML_PATH}.'
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
        output_wordslist(wordslist_path, kanji_yomi_dict, kanji_ydkey_map)
    
    # generate wiktionary detail
    if args.wiktionary:
        html_src_dir = os.path.join(args.input_wiki_cache_dir, 'html')
        convert_wikt_to_html(html_src_dir, args.html_output_path)

def regist_kanji_detail(sub_parsers):
    add_wordslist_args(sub_parsers)
    return {'kanji': genereate_kanji_detail}