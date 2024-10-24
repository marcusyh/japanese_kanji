import os
import shutil
from file_util import prepare_file_path
   
def deploy_data(args, src_config, dst_config, suffix=''):
    update_data_all = not (args.update_onyomi or args.update_kunyomi or args.update_wordslist or args.update_wiktionary)
    remove_existing_files = args.remove_existing_files and update_data_all
    
    # The path to deploy data
    data_deploy_path = os.path.join(args.deploy_path, dst_config.DATA_ROOT_DIR)
    prepare_file_path(data_deploy_path, is_dir=True, delete_if_exists=remove_existing_files,  create_if_not_exists=True)

    # copy data
    if update_data_all or args.update_onyomi or args.update_kunyomi:
        dst_pron_list_path = os.path.join(args.deploy_path, dst_config.PRON_LIST_DIR)
        prepare_file_path(dst_pron_list_path, is_dir=True, delete_if_exists=False, create_if_not_exists=True)
        
        for filename in os.listdir(src_config.MARKDOWN_PATH):
            if (args.update_onyomi or update_data_all) and filename.startswith(src_config.ONYOMI_FILENAME):
                shutil.copy(
                    os.path.join(src_config.MARKDOWN_PATH, filename),
                    os.path.join(dst_pron_list_path, filename)
                )
            if (args.update_kunyomi or update_data_all) and filename.startswith(src_config.KUNYOMI_FILENAME):
                shutil.copy(
                    os.path.join(src_config.MARKDOWN_PATH, filename),
                    os.path.join(dst_pron_list_path, filename)
                )
    
    if update_data_all or args.update_wiktionary:
        dst_kanji_wikt_path = os.path.join(args.deploy_path, dst_config.KANJI_WIKT_DIR)
        shutil.copytree(src_config.HTML_PATH, dst_kanji_wikt_path, dirs_exist_ok=True)

    if args.update_wordslist or update_data_all:
        src_words_path = os.path.join(src_config.OUTPUT_ROOT, f'{src_config.WORDS_FILENAME}.json')
        dst_words_path = os.path.join(args.deploy_path, dst_config.WORDS_LIST_FILE)
        shutil.copy(src_words_path, dst_words_path)
