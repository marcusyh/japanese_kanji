import argparse
import os
from preparation import prepare_kanji_data

def boolean_arg(value):
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError(f"Boolean value expected, got: {value}")

def kanji_type_list(value):
    valid_types = ['jouyou', 'jinmei', 'hyougai', 'itai']
    types = [t.strip().lower() for t in value.split(',')]
    if not all(t in valid_types for t in types):
        raise argparse.ArgumentTypeError(f"Invalid kanji type. Valid types are: {', '.join(valid_types)}")
    print(value, types)
    return types


def add_prepare_kanji_args(sub_parsers):
    prepare_parser = sub_parsers.add_parser(
        'prepare',
        help='Prepare kanji data',
        description='Prepare and save kanji data with various options.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    prepare_parser.add_argument(
        '-f', '--format',
        choices=['csv', 'docx'],
        default='csv',
        help='Output file format (csv or docx, default: csv)'
    )
    prepare_parser.add_argument(
        '-t', '--with_tag',
        type=boolean_arg,
        default=True,
        help='Include tags in the output (default: True)'
    )
    prepare_parser.add_argument(
        '-k', '--kanji_types',
        type=kanji_type_list,
        default=['jouyou', 'jinmei', 'hyougai', 'itai'],
        help='Comma-separated list of kanji types to include (default: all types)'
    )
    prepare_parser.add_argument(
        '-o', '--output_file_path',
        type=str,
        default='../data/preparation/output.csv',
        help='Output file path (default: ../data/preparation/output.csv)'
    )
    prepare_parser.add_argument(
        '-s', '--source_data_dir',
        type=str,
        default='../data/preparation',
        help='Source data directory (default: ../data/preparation)'
    )

def preparation_wrapper(args):
    # Check if the output file extension matches the specified format
    _, file_extension = os.path.splitext(args.output_file_path)
    if file_extension[1:].lower() != args.format.lower():
        raise argparse.ArgumentTypeError(f"Output file extension '{file_extension}' does not match the specified format '{args.format}'")

    # Prepare kanji_types dictionary
    kanji_types = {
        'jouyou': 'jouyou' in args.kanji_types,
        'jinmei': 'jinmei' in args.kanji_types,
        'hyougai': 'hyougai' in args.kanji_types,
        'itai': 'itai' in args.kanji_types,
    }

    # Add additional arguments
    additional_args = {
        'source_data_dir': args.source_data_dir,
        'with_tag': args.with_tag,
        'output_file_path': args.output_file_path,
        'format': args.format
    }

    # Call prepare_kanji_data with all necessary arguments
    prepare_kanji_data(args, **kanji_types)


def regist_preparation(sub_parsers):
    add_prepare_kanji_args(sub_parsers)
    #prepare_parser.set_defaults(func=lambda args: prepare_kanji_data(args))
    return {'prepare': preparation_wrapper}
