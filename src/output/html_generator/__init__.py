import shutil
import os
import json
from file_util import prepare_output_path


def generate_words_json(merged_kanji_info, kanji_ydkey_map):
    words_dict = {}
    for kanji, primary_key in kanji_ydkey_map.items():
        if primary_key not in merged_kanji_info or 'ja' not in merged_kanji_info[primary_key]:
            words_dict[kanji] = {}
            continue
        words_dict[kanji] = {}
        
        onyomi_list = []
        x = merged_kanji_info[primary_key]['ja']
        if '音読み' in merged_kanji_info[primary_key]['ja']:
            for reading_type, readings in merged_kanji_info[primary_key]['ja']['音読み'].items():
                if '表内' not in readings:
                    continue
                for pron_dict in readings['表内']:
                    new_pron = {}
                    if 'pron' in pron_dict:
                        pron = pron_dict['pron']
                        new_pron = {
                            'pron': pron,
                            'type': reading_type
                        }
                    if 'words_list' in pron_dict:
                        new_pron['words_list'] = pron_dict['words_list']
                    if new_pron:
                        onyomi_list.append(new_pron)
                        
        kunyomi_list = []
        if '訓読み' in merged_kanji_info[primary_key]['ja']:
            kunyomi_ori = merged_kanji_info[primary_key]['ja']['訓読み']
            if '表内' in kunyomi_ori:
                for pron_dict in kunyomi_ori['表内']:
                    new_pron = {}
                    if 'pron' in pron_dict:
                        pron = pron_dict['pron']
                        new_pron = {
                            'pron': pron,
                        }
                    if 'words_list' in pron_dict:
                        new_pron['words_list'] = pron_dict['words_list']
                    if new_pron:
                        kunyomi_list.append(new_pron)
                        
        words_dict[kanji] = {
            "音読み": onyomi_list,
            "訓読み": kunyomi_list
        }
        
    return words_dict
        
        

def save_json_file(words_dict, output_dir):
    # create words json dir
    words_json_path = os.path.join(output_dir, 'data', 'words_list.json')
    with open(words_json_path, 'w', encoding='utf-8') as f:
        json.dump(words_dict, f, ensure_ascii=False, indent=4)
    


def generate_html(
        output_filepath,
        merged_kanji_info, 
        kanji_ydkey_map 
    ):
    # create html dir
    output_dir = os.path.dirname(os.path.dirname(output_filepath))
    prepare_output_path(output_dir)

    # copy html template
    shutil.copytree('output/html_generator/template', output_dir)
    
    # generate words json
    words_dict = generate_words_json(merged_kanji_info, kanji_ydkey_map)
    save_json_file(words_dict, output_dir)