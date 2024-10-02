import argparse
from parser.ja_onyomi.args import regist_ja_onyomi

def regist_parser(sub_commands):
    sub_parser = sub_commands.add_parser(
        'parse',
        help='Process cached wiktionary data',
        description='Process and display cached wiktionary data with various options.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    third_level_parser = sub_parser.add_subparsers(dest='command', help='Available commands')
    
    register = {}
    
    register.update(regist_ja_onyomi(third_level_parser))

    return register