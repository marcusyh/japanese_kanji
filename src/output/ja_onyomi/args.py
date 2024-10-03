import argparse
from output.ja_onyomi import output_ja_onyomi

def add_onyomi_args(sub_parsers):
    onyomi_parser = sub_parsers.add_parser(
        'onyomi',
        help='Process onyomi data',
        description='Process and display onyomi data with various options.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    onyomi_parser.add_argument(
        '-w', '--wiki_cache_dir',
        type=str,
        default='../data/wiktionary',
        help='Path to the wiki cache. (default: ../data/wiktionary)'
    )
    onyomi_parser.add_argument(
        '-y', '--include_hyogai',
        action='store_true',
        help='Include hyogai kanji in the output. By default, include only the 表内 pronunciation.'
    )
    onyomi_parser.add_argument(
        '-o', '--show_old_pron',
        action='store_true',
        help='Show old Jpanese pronunciations in the output. By default, show only the modern Japanese pronunciation.'
    )
    onyomi_parser.add_argument(
        '-d', '--duplicate_by_all',
        action='store_true',
        help='Duplicate entries by all pronunciations. By default, output only one entry for each group.'
    )
    onyomi_parser.add_argument(
        '-f', '--filepath',
        type=str,
        default='../data/parsed_result/ja_onyomi.md',
        help='Path to the output file containing onyomi data. If not specified, defaults to ../data/parsed_result/ja_onyomi.md for Markdown or ../data/parsed_result/ja_onyomi.csv for CSV.'
    )
    onyomi_parser.add_argument(
        '-c', '--is_csv',
        action='store_true',
        help='Output in CSV format when this option is specified. By default, output in Markdown format.'
    )

    
def output_onyomi_wrapper(args):
    if args.is_csv:
        args.filepath = args.filepath.replace('.md', '.csv')
    output_ja_onyomi(args)


def regist_ja_onyomi(sub_parsers):
    add_onyomi_args(sub_parsers)
    return {'onyomi': output_onyomi_wrapper}