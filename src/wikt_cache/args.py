import argparse
from wikt_cache import fetch_wikt_cache

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
        default='../data/wiktionary/cache.txt',
        help='Path to the Wiktionary cache file. (default: ../data/wiktionary/cache.txt)'
    )
    wikt_parser.add_argument(
        '-s', '--source_data_dir',
        type=str,
        default='../data/preparation',
        help='Path to the source data directory. (default: ../data/preparation)'
    )

def process_wikt_wrapper(args):
    fetch_wikt_cache(
        source_data_dir=args.source_data_dir,
        cache_path=args.cache_path,
        update_flag=args.update_flag,
        fetch_missing_only=args.fetch_missing_only
    )

def regist_wiktionary(sub_parsers):
    add_wikt_args(sub_parsers)
    return {'wikt': process_wikt_wrapper}