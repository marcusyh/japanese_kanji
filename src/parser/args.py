import argparse
from wiktionary.ja.onyomi import process_onyomi

def boolean_arg(value):
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError(f"Boolean value expected, got: {value}")

def add_onyomi_args(sub_parsers):
    onyomi_parser = sub_parsers.add_parser(
        'onyomi',
        help='Process onyomi data',
        description='Process and display onyomi data with various options.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    onyomi_parser.add_argument(
        '-y', '--include_hyogai',
        type=boolean_arg,
        default=False,
        help='Include hyogai kanji in the output. (default: False)'
    )
    onyomi_parser.add_argument(
        '-o', '--show_old_pron',
        type=boolean_arg,
        default=False,
        help='Show old pronunciations in the output. (default: False)'
    )
    onyomi_parser.add_argument(
        '-a', '--include_all_prons',
        type=boolean_arg,
        default=False,
        help='Include all pronunciations in the output. (default: False)'
    )
    onyomi_parser.add_argument(
        '-d', '--duplicate_by_all',
        type=boolean_arg,
        default=False,
        help='Duplicate entries by all pronunciations. (default: False)'
    )
    onyomi_parser.add_argument(
        '-f', '--filepath',
        type=str,
        default=None,
        help='Path to the input file containing onyomi data. (default: None)'
    )
    onyomi_parser.add_argument(
        '-m', '--is_markdown',
        type=boolean_arg,
        default=False,
        help='Output in Markdown format. (default: False)'
    )


def process_onyomi_wrapper(args):
    # This function will be called with the parsed arguments
    # You'll need to modify the process_onyomi function to accept these arguments
    process_onyomi(
        args.filepath,
        include_hyogai=args.include_hyogai,
        show_old_pron=args.show_old_pron,
        include_all_prons=args.include_all_prons,
        duplicate_by_all=args.duplicate_by_all,
        is_markdown=args.is_markdown
    )

def register_commands(sub_parsers):
    add_onyomi_args(sub_parsers)
    return {'onyomi': process_onyomi_wrapper}