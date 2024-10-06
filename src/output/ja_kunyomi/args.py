import argparse
import os
from output import config
from output.ja_kunyomi import output_ja_kunyomi

markdown_file_path = os.path.join(config.MARKDOWN_PATH, f'{config.KUNYOMI_FILENAME}.md')
csv_file_path = os.path.join(config.CSV_PATH, f'{config.KUNYOMI_FILENAME}.csv')


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
        default=config.WIKT_CACHE_DIR,
        help='Path to the wiki cache. (default: ../data/wiktionary)'
    )
    kunyomi_parser.add_argument(
        '-f', '--output_path',
        type=str,
        default=markdown_file_path,
        help=f'Path to the output file containing kunyomi data. If not specified, defaults to {markdown_file_path} for Markdown or {csv_file_path} for CSV.'
    )
    kunyomi_parser.add_argument(
        '-c', '--output_format',
        type=str,
        default='markdown',
        choices=['markdown', 'csv'],
        help='Output format. The value must be markdown or csv. By default, output in Markdown format.'
    )
    kunyomi_parser.add_argument(
        '-d', '--show_duplicated',
        action='store_true',
        help='show all duplicate entries by all pronunciations. By default, output only one entry for each group.'
    )

    
def output_kunyomi_wrapper(args):
    if args.output_format == 'csv':
        args.output_path = args.output_path.replace('.md', '.csv')
    output_ja_kunyomi(args)


def regist_ja_kunyomi(sub_parsers):
    add_kunyomi_args(sub_parsers)
    return {'kunyomi': output_kunyomi_wrapper}