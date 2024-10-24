import argparse
import os
import config
from output.ja_onyomi import output_ja_onyomi

def add_onyomi_args(sub_parsers):
    onyomi_parser = sub_parsers.add_parser(
        'onyomi',
        help='Process onyomi data',
        description='Process and display onyomi data with various options.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    onyomi_parser.add_argument(
        '-w', '--input_wiki_cache_dir',
        type=str,
        default=config.WIKT_CACHE_DIR,
        help=f'Path to the wiki cache. (default: {config.WIKT_CACHE_DIR})'
    )
    onyomi_parser.add_argument(
        '-f', '--output_dir',
        type=str,
        default=config.MARKDOWN_PATH,
        help=f'Path to the output directory containing all data. If not specified, defaults to {config.MARKDOWN_PATH} for Markdown or {config.CSV_PATH} for CSV.'
    )
    onyomi_parser.add_argument(
        '-c', '--output_format',
        type=str,
        default='markdown',
        choices=['markdown', 'csv'],
        help='Output format. The value must be markdown, csv. By default, output in Markdown format.'
    )
    onyomi_parser.add_argument(
        '-by', '--group_by',
        type=str,
        default='all',
        choices=['merge', 'all', 'go_kan'],
        help='Group by.'
    )
    onyomi_parser.add_argument(
        '-y', '--merge_hyogai',
        action='store_true',
        help='Merge hyougai kanji to rows for group by and sort by all pronunciations. By default, hyougai pronunciations are not included.'
    )
    onyomi_parser.add_argument(
        '-o', '--show_old_pron',
        action='store_true',
        help='Show old Jpanese pronunciations in the output. By default, show only the modern Japanese pronunciation.'
    )
    onyomi_parser.add_argument(
        '-g', '--show_hyogai',
        action='store_true',
        help='Show hyougai pronunciation in the additional column for reference.'
    )
    onyomi_parser.add_argument(
        '-go', '--show_hyogai_old',
        action='store_true',
        help='Merge old hyougai pronunciation to old pronunciation column. By default, old hyougai pronunciation is not included.'
    )
    onyomi_parser.add_argument(
        '-d', '--show_duplicated',
        action='store_true',
        help='show all duplicate entries by all pronunciations. By default, output only one entry for each group.'
    )

def output_ja_onyomi_wrapper(args):
    if args.output_format == 'csv' and args.output_dir == config.MARKDOWN_PATH:
        args.output_dir = config.CSV_PATH
    output_ja_onyomi(args)


def regist_ja_onyomi(sub_parsers):
    add_onyomi_args(sub_parsers)
    return {'onyomi': output_ja_onyomi_wrapper}