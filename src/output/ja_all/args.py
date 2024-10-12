import argparse
import os
import config
from output.ja_all import output_ja_all

def add_all_args(sub_parsers):
    all_parser = sub_parsers.add_parser(
        'all',
        help='Process all data',
        description='Process and display all data with various options.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    all_parser.add_argument(
        '-w', '--input_wiki_cache_dir',
        type=str,
        default=config.WIKT_CACHE_DIR,
        help=f'Path to the wiki cache. (default: {config.WIKT_CACHE_DIR})'
    )
    all_parser.add_argument(
        '-f', '--output_dir',
        type=str,
        default=config.MARKDOWN_PATH,
        help=f'Path to the output directory containing all data. If not specified, defaults to {config.MARKDOWN_PATH} for Markdown or {config.CSV_PATH} for CSV.'
    )
    all_parser.add_argument(
        '-c', '--output_format',
        type=str,
        default='markdown',
        choices=['markdown', 'csv'],
        help='Output format. The value must be markdown, csv. By default, output in Markdown format.'
    )
    all_parser.add_argument(
        '-y', '--merge_hyogai',
        action='store_true',
        help='Merge hyougai kanji to rows for group by and sort by all pronunciations. By default, hyougai pronunciations are not included.'
    )
    all_parser.add_argument(
        '-o', '--show_old_pron',
        action='store_true',
        help='Show old Jpanese pronunciations in the output. By default, show only the modern Japanese pronunciation.'
    )
    all_parser.add_argument(
        '-g', '--show_hyogai',
        action='store_true',
        help='Show hyougai pronunciation in the additional column for reference.'
    )
    all_parser.add_argument(
        '-go', '--show_hyogai_old',
        action='store_true',
        help='Merge old hyougai pronunciation to old pronunciation column. By default, old hyougai pronunciation is not included.'
    )
    all_parser.add_argument(
        '-d', '--show_duplicated',
        action='store_true',
        help='show all duplicate entries by all pronunciations. By default, output only one entry for each group.'
    )

    
def regist_ja_all(sub_parsers):
    add_all_args(sub_parsers)
    return {'all': output_ja_all}