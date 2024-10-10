import argparse
import config
from wikt_cache import fetch_wikt_cache
from wikt_cache.wiki_html import fetch_wiki_html

def boolean_arg(value):
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError(f"Boolean value expected, got: {value}")

def add_wikt_args(sub_parsers):
    wikt_parser = sub_parsers.add_parser(
        'wikt',
        help='Fetch Wiktionary cache',
        description='Fetch and update Wiktionary cache for kanji data.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    wikt_parser.add_argument(
        '-ht', '--update_html',
        action='store_true',
        help='Wikitext cache will be update or fetch by default. If this argument is specified, html will be updated or fetched.'
    )
    wikt_parser.add_argument(
        '-u', '--update_flag',
        type=boolean_arg,
        default=False,
        help='Update all entries in the cache. (default: False)'
    )
    wikt_parser.add_argument(
        '-f', '--fetch_missing_only',
        type=boolean_arg,
        default=True,
        help='Fetch only missing entries. (default: True)'
    )
    wikt_parser.add_argument(
        '-c', '--cache_path',
        type=str,
        default=config.WIKT_CACHE_FILE,
        help=f'Path to the Wiktionary cache file. (default: {config.WIKT_CACHE_FILE})'
    )
    wikt_parser.add_argument(
        '-s', '--source_data_dir',
        type=str,
        default=config.PREPARATION_DIR,
        help=f'Path to the source data directory. (default: {config.PREPARATION_DIR})'
    )

def process_wikt_wrapper(args):
    if not args.update_html:
        fetch_wikt_cache(
            source_data_dir=args.source_data_dir,
            cache_path=args.cache_path,
            update_flag=args.update_flag,
            fetch_missing_only=args.fetch_missing_only
        )
    else:
        fetch_wiki_html(
            cache_path=config.WIKT_CACHE_DIR,
            update_flag=args.update_flag,
            fetch_missing_only=args.fetch_missing_only
        )

def regist_wiktionary(sub_parsers):
    add_wikt_args(sub_parsers)
    return {'wikt': process_wikt_wrapper}