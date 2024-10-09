import argparse
from output.ja_onyomi.args import regist_ja_onyomi
from output.ja_kunyomi.args import regist_ja_kunyomi
from output.kanji import regist_kanji_detail
from output.ja_all.args import regist_ja_all

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
    register.update(regist_ja_kunyomi(third_level_parser))
    register.update(regist_kanji_detail(third_level_parser))
    register.update(regist_ja_all(third_level_parser))

    return register