import argparse
from output.ja_kunyomi import output_ja_kunyomi

markdown_path = '../data/parsed_result/markdown/ja_kunyomi.md'
csv_path = '../data/parsed_result/csv/ja_kunyomi.csv'
html_path = '../data/parsed_result/html/data/日本語_訓読み表.md'

def add_kunyomi_args(sub_parsers):
    kunyomi_parser = sub_parsers.add_parser(
        'kunyomi',
        help='Process kunyomi data',
        description='Process and display kunyomi data with various options.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    kunyomi_parser.add_argument(
        '-w', '--input_wiki_cache_dir',
        type=str,
        default='../data/wiktionary',
        help='Path to the wiki cache. (default: ../data/wiktionary)'
    )
    kunyomi_parser.add_argument(
        '-f', '--output_path',
        type=str,
        default=markdown_path,
        help=f'Path to the output file containing kunyomi data. If not specified, defaults to {markdown_path} for Markdown or {csv_path} for CSV or {html_path} for HTML.'
    )
    kunyomi_parser.add_argument(
        '-c', '--output_format',
        type=str,
        default='markdown',
        choices=['markdown', 'csv', 'html'],
        help='Output format. The value must be markdown, csv or html. By default, output in Markdown format.'
    )
    kunyomi_parser.add_argument(
        '-d', '--show_duplicated',
        action='store_true',
        help='show all duplicate entries by all pronunciations. By default, output only one entry for each group.'
    )

    
def output_kunyomi_wrapper(args):
    if args.output_format == 'csv':
        args.output_path = args.output_path.replace('.md', '.csv')
    elif args.output_format == 'html':
        if not args.output_path or args.output_path == markdown_path or args.output_path == csv_path:
            args.output_path = html_path
    output_ja_kunyomi(args)


def regist_ja_kunyomi(sub_parsers):
    add_kunyomi_args(sub_parsers)
    return {'kunyomi': output_kunyomi_wrapper}