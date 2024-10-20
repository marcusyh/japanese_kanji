import argparse
from output.copier import config as copier_config
import config
from output.copier.copier import deploy_data
   
def add_copier_args(sub_parsers):
    copier_parser = sub_parsers.add_parser(
        'copy',
        help='Copy all generated result to specified path',
        description='Copy all generated markdown result to specified path',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    copier_parser.add_argument(
        '-o', '--update_onyomi',
        action='store_true',
        help='Update onyomi markdown files.'
    )
    copier_parser.add_argument(
        '-k', '--update_kunyomi',
        action='store_true',
        help='Update kunyomi markdown files.'
    )
    copier_parser.add_argument(
        '-w', '--update_wordslist',
        action='store_true',
        help='Update words_list.json.'
    )
    copier_parser.add_argument(
        '-wk', '--update_wiktionary',
        action='store_true',
        help='Update wiktionary html files.'
    )
    copier_parser.add_argument(
        '-r', '--remove_existing_files',
        action='store_true',
        help='Remove existing files.'
    )
    copier_parser.add_argument(
        '-p', '--deploy_path',
        type=str,
        default=config.JA_WEB_DEPLOY_DIR,
        help='Path to the output directory, the default path is ' + config.JA_WEB_DEPLOY_DIR
    )
    
def deploy_data_wrapper(args):
    deploy_data(args, config, copier_config)
    

def regist_copier_args(sub_parsers):
    add_copier_args(sub_parsers)
    return {'copy': deploy_data_wrapper}