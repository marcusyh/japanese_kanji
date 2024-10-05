import argparse
from output.ja_onyomi import output_ja_onyomi

markdown_path = '../data/parsed_result/markdown/ja_onyomi.md'
csv_path = '../data/parsed_result/csv/ja_onyomi.csv'
html_path = '../data/parsed_result/html/data/日本語_音読み表.md'

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
        default='../data/wiktionary',
        help='Path to the wiki cache. (default: ../data/wiktionary)'
    )
    onyomi_parser.add_argument(
        '-f', '--output_path',
        type=str,
        default=markdown_path,
        help=f'Path to the output file containing onyomi data. If not specified, defaults to {markdown_path} for Markdown or {csv_path} for CSV or {html_path} for HTML.'
    )
    onyomi_parser.add_argument(
        '-c', '--output_format',
        type=str,
        default='markdown',
        choices=['markdown', 'csv', 'html'],
        help='Output format. The value must be markdown, csv or html. By default, output in Markdown format.'
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
        '-d', '--show_duplicated',
        action='store_true',
        help='show all duplicate entries by all pronunciations. By default, output only one entry for each group.'
    )

    
def output_onyomi_wrapper(args):
    if args.output_format == 'csv':
        args.output_path = args.output_path.replace('.md', '.csv')
    elif args.output_format == 'html':
        if not args.output_path or args.output_path == markdown_path or args.output_path == csv_path:
            args.output_path = html_path
    output_ja_onyomi(args)


def regist_ja_onyomi(sub_parsers):
    add_onyomi_args(sub_parsers)
    return {'onyomi': output_onyomi_wrapper}