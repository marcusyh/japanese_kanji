import os
import shutil
import argparse
from output import config
from file_util import prepare_file_path
   
def boolean_arg(value):
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError(f"Boolean value expected, got: {value}")

def add_webui_args(sub_parsers):
    webui_parser = sub_parsers.add_parser(
        'webui',
        help='Deploy all generated markdown result to WebUI',
        description='Generate and deploy webUI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    webui_parser.add_argument(
        '-t', '--update_template',
        action='store_true',
        help='Update html, js and css by new template.'
    )
    webui_parser.add_argument(
        '-s', '--update_http_server',
        action='store_true',
        help='Update http_server.py.'
    )
    webui_parser.add_argument(
        '-d', '--update_data',
        action='store_true',
        help='Update yomi markdown files and words_list.json.'
    )
    webui_parser.add_argument(
        '-r', '--remove_existing_files',
        type=boolean_arg,
        default=True,
        help='Remove existing files. (default: True)'
    )
    webui_parser.add_argument(
        '-p', '--deploy_path',
        type=str,
        default=config.WEBUI_DEPLOY_DIR,
        help='Path to the output directory, the default path is ' + config.WEBUI_DEPLOY_DIR
    )
    
def deploy_template(args):
    # The root path to deploy webUI
    webUI_deploy_path = os.path.join(args.deploy_path, 'webUI')
    # create webui dir
    prepare_file_path(webUI_deploy_path, is_dir=True, delete_if_exists=args.remove_existing_files)
    # copy html template and http server
    shutil.copytree('webUI/template', webUI_deploy_path, dirs_exist_ok=True)
    # Create a symbolic link to data_deploy_path in webUI_deploy_path/data

    data_deploy_path = '../data'
    data_link_path = os.path.join(webUI_deploy_path, 'data')
    # Remove existing symlink if it exists
    if os.path.islink(data_link_path):
        os.unlink(data_link_path)
    # Create the new symlink
    os.symlink(data_deploy_path, data_link_path, target_is_directory=True)
    print(f"Created symbolic link: {data_link_path} -> {data_deploy_path}")
            

def deploy_http_server(args):
    # The path to deploy http_server.py
    http_server_deploy_path = os.path.join(args.deploy_path, 'http_server.py')
    # delete http_server.py if exists
    prepare_file_path(http_server_deploy_path, is_dir=False, delete_if_exists=args.remove_existing_files)
    # copy http_server.py
    shutil.copy('webUI/http_server.py', http_server_deploy_path)
    

def deploy_data(args):
    # The path to deploy data
    data_deploy_path = os.path.join(args.deploy_path, 'data')
    # delete data dir if exists
    prepare_file_path(data_deploy_path, is_dir=True, delete_if_exists=args.remove_existing_files)
    # copy data
    shutil.copytree(config.MARKDOWN_PATH, data_deploy_path, dirs_exist_ok=True)


def deploy_update_webui(args):
    # If no specific update flags are set, update everything
    update_all = not (args.update_template or args.update_http_server or args.update_data)

    if update_all or args.update_http_server:
        deploy_http_server(args)
    
    if update_all or args.update_data:
        deploy_data(args)
        
    if update_all or args.update_template:
        deploy_template(args)
   

def regist_webui_args(sub_parsers):
    add_webui_args(sub_parsers)
    return {'webui': deploy_update_webui}