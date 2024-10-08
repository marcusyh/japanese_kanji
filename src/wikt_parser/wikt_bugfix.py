import copy
from wikt_cache.patch import load_patch
from preparation.parser import load_preparation_data


def fix_by_wikt_patch(wikt_onyomi_dict):
    """
    Apply patches to the Wiktionary on'yomi dictionary using a predefined patch file.

    This function updates the on'yomi readings in the Wiktionary dictionary with
    information from a patch file, which may contain corrections data.

    Args:
        wikt_onyomi_dict (dict): The Wiktionary on'yomi dictionary to be patched.

    Returns:
        None: The function modifies the input dictionary in-place.
    """
    # Load the patch data
    patch_pron_arch = load_patch()
    
    # Iterate through each kanji entry in the Wiktionary dictionary
    for kanji, pron_arch in wikt_onyomi_dict.items():
        raw_kanji = kanji[0]  # Extract the first character as the raw kanji
        
        # Skip if the kanji is not in the patch data
        if raw_kanji not in patch_pron_arch:
            continue
        
        # Skip if there's no Japanese data for this kanji in the patch
        if 'ja' not in patch_pron_arch[raw_kanji]:
            continue
        
        # Skip if there's no on'yomi data for this kanji in the patch
        if '音読み' not in patch_pron_arch[raw_kanji]['ja']:
            continue
        
        # Get the on'yomi patch data for this kanji
        onyomi_patch = patch_pron_arch[raw_kanji]['ja']['音読み']

        # Apply the patch data to the Wiktionary entry
        for reading_type, value in onyomi_patch.items():
            if reading_type not in pron_arch['ja']['音読み']:
                # If the reading type doesn't exist, add it
                pron_arch[reading_type] = value
            else:
                # If the reading type exists, extend the existing list with new values
                pron_arch[reading_type].extend(value)
                

def merge_wikt_onyomi_dict(wikt_onyomi_dict_all, wikt_onyomi_dict_delta):
    """
    Merge two Wiktionary on'yomi dictionaries, updating the first with data from the second.

    This function combines information from two dictionaries containing on'yomi (音読み) readings,
    prioritizing existing data in the first dictionary and adding new information from the second.

    Args:
        wikt_onyomi_dict_all (dict): The main dictionary to be updated.
        wikt_onyomi_dict_delta (dict): The dictionary containing new or additional information.

    Returns:
        None: The function modifies wikt_onyomi_dict_all in-place.
    """
    for reading_type, rt_value in wikt_onyomi_dict_delta.items():
        # Add reading_type to wikt_onyomi_dict_all if it doesn't exist
        if reading_type not in wikt_onyomi_dict_all:
            wikt_onyomi_dict_all[reading_type] = rt_value
            continue

        for category, c_value in rt_value.items():
            # Add category to wikt_onyomi_dict_all[reading_type] if it doesn't exist
            if category not in wikt_onyomi_dict_all[reading_type]:
                wikt_onyomi_dict_all[reading_type][category] = c_value
                continue
            
            # Add new items to wikt_onyomi_dict_all[reading_type][category]
            for item in c_value:
                if item not in wikt_onyomi_dict_all[reading_type][category]:
                    wikt_onyomi_dict_all[reading_type][category].append(item)
        
        # create new category to delete duplicated items in '表外' if exists in '表内'
        if len(wikt_onyomi_dict_all[reading_type]) <= 1:
            continue
        new_hyogai = []
        for item in wikt_onyomi_dict_all[reading_type]['表外']:
            if item not in wikt_onyomi_dict_all[reading_type]['表内']:
                new_hyogai.append(item)
        wikt_onyomi_dict_all[reading_type]['表外'] = new_hyogai
        

def merge_exists_wikt_onyomi_by_prpr_itai_group(prpr_itai_kanji_list, wikt_onyomi_dict):
    """
    Merge Wiktionary on'yomi information for groups of itai (異体字) kanji.

    This function combines on'yomi (音読み) readings from the Wiktionary dictionary
    for groups of itai kanji (characters with the same meaning and pronunciation
    but different written forms). It processes each group of itai kanji from the
    prpr_itai_kanji_list and merges their corresponding on'yomi information from
    the wikt_onyomi_dict.

    Args:
        prpr_itai_kanji_list (list): A list of kanji, where each kanji is an
                                     itai variant of each other.
        wikt_onyomi_dict (dict): The Wiktionary dictionary containing on'yomi
                                 information for individual kanji.

    Returns:
        dict: A single merged on'yomi information dictionary for one group of
              itai kanji. This dictionary combines the on'yomi readings from
              all kanji in the group, removing duplicates.

    Note:
        - The function only returns the merged value (on'yomi information) for
          a single group of itai kanji, not the entire dictionary for all groups.
        - The key for this merged information (a string concatenation of all
          kanji in the group) is generated elsewhere in the code.

    Example:
        Input:
        prpr_itai_kanji_list = [['峰', '峯']]
        wikt_onyomi_dict = {
            '峰': {'音読み': {'表内': [{'pron': 'ホウ'}]}},
            '峯': {'音読み': {'表内': [{'pron': 'ホウ'}, {'pron': 'ブ'}]}}
        }

        Output:
        {'音読み': {'表内': [{'pron': 'ホウ'}, {'pron': 'ブ'}]}}
    """
    merged_onyomi_dict = {}

    # Process each kanji in the kanji_dict
    for kanji in prpr_itai_kanji_list:
        # Check for different possible keys in the Wiktionary dictionary
        for tail in ['', '1', '2', '3']:
            wikt_key = f'{kanji}{tail}'
            if wikt_key not in wikt_onyomi_dict:
                continue
            
            # Initialize new_onyomi_info if it's empty
            if not merged_onyomi_dict:
                merged_onyomi_dict = wikt_onyomi_dict[wikt_key]
                continue
            
            # Skip if the information is identical
            if merged_onyomi_dict == wikt_onyomi_dict[wikt_key]:
                continue
            
            # Merge the on'yomi information
            merge_wikt_onyomi_dict(merged_onyomi_dict, wikt_onyomi_dict[wikt_key])
            
    return merged_onyomi_dict
 

def fix_by_preparation(wikt_onyomi_dict_all, prpr_onyomi_dict):
    """
    Fix the on'yomi dictionary using preparation data as the Wiktionary data has lots of inaccurate data.

    This function compares the Wiktionary on'yomi data with the preparation data and creates a new,
    corrected on'yomi dictionary. It categorizes readings as either '表内' (standard) or '表外' (non-standard)
    based on their presence in the preparation data.

    Args:
        wikt_onyomi_dict_all (dict): The Wiktionary on'yomi dictionary to be fixed.
        prpr_onyomi_dict (dict): The preparation data containing accurate on'yomi information.

    Returns:
        dict: A new dictionary containing the corrected on'yomi information.
    """
    # if no preparation data, return the original dictionary
    if '音読み' not in prpr_onyomi_dict:
        return wikt_onyomi_dict_all

    prpr_onyomi_list = list(prpr_onyomi_dict['音読み'].keys())
    prpr_onyomi_matched_list = []
    new_onyomi_dict_all = {}
    
    # Process both '表内' and '表外' categories
    for category in ['表内', '表外']:
        for reading_type, rt_value in wikt_onyomi_dict_all.items(): # reading_type: 呉音, 漢音, 慣用音, etc
            if category not in rt_value:
                continue
            for item in rt_value[category]: # item: {'pron': 'ホウ', 'old_pron': 'ホウ'}
                if 'pron' not in item:
                    continue
                
                # If the pronunciation is in the preparation data, add to '表内'
                if item['pron'] in prpr_onyomi_list: # item['pron']: ホウ
                    prpr_onyomi_matched_list.append(item['pron'])
                    prpr_onyomi_list.remove(item['pron'])
                    
                    # Add to '表内' in the new dictionary
                    if reading_type not in new_onyomi_dict_all:
                        new_onyomi_dict_all[reading_type] = {}
                    if '表内' not in new_onyomi_dict_all[reading_type]:
                        new_onyomi_dict_all[reading_type]['表内'] = []
                    new_item = copy.deepcopy(item) # item: {'pron': 'ホウ', 'old_pron': 'ホウ'}
                    new_item['words_list'] = copy.deepcopy(prpr_onyomi_dict['音読み'][item['pron']]) # item['words_list']: ['哀れ', '哀れな話', '哀れがる']
                    new_onyomi_dict_all[reading_type]['表内'].append(new_item)
                else:
                    # If the pronunciation is not in the preparation data, add to '表外'
                    # Add to '表外' in the new dictionary
                    if reading_type not in new_onyomi_dict_all:
                        new_onyomi_dict_all[reading_type] = {}
                    if '表外' not in new_onyomi_dict_all[reading_type]:
                        new_onyomi_dict_all[reading_type]['表外'] = []
                    new_onyomi_dict_all[reading_type]['表外'].append(copy.deepcopy(item))
        
        # Break if all preparation data has been processed
        if len(prpr_onyomi_list) == 0:
            break
    
    # Add any remaining preparation data as '慣用音' (customary readings)
    for pron in prpr_onyomi_list:
        if '慣用音' not in new_onyomi_dict_all:
            new_onyomi_dict_all['慣用音'] = {}
        if '表内' not in new_onyomi_dict_all['慣用音']:
            new_onyomi_dict_all['慣用音']['表内'] = []
        new_onyomi_dict_all['慣用音']['表内'].append({
            'pron': pron,
            "words_list": prpr_onyomi_dict['音読み'][pron]
        })
    
    return new_onyomi_dict_all


def get_kunyomi_from_preparation(prpr_yomi_dict):
    """
    Get kun'yomi from preparation data.

    Args:
        prpr_yomi_dict (dict): The preparation data containing kun'yomi information.

    Returns:
        dict: A dictionary containing kun'yomi information.
        
    input example:
    {
        "訓読み": {
            'あわれ': ['哀れ', '哀れな話', '哀れがる'],
            'あわれむ': ['哀れむ', '哀れみ']
        }
    }
    output example:
    {
        "表内": [
            {"pron": "あわれ", "words_list": ['哀れ', '哀れな話', '哀れがる']},
            {"pron": "あわれむ", "words_list": ['哀れむ', '哀れみ']}
        ]
    }
    """
    if '訓読み' not in prpr_yomi_dict:    
        return {}
    
    kunyomi_dict = {"表内": []}
    for pron, words_list in prpr_yomi_dict['訓読み'].items():
        kunyomi_dict["表内"].append({
            "pron": pron,
            "words_list": words_list
        })
    
    return kunyomi_dict
    

def merge_with_preparation(wikt_onyomi_dict, add_mark_flag=True):
    """
    Merge Wiktionary on'yomi dictionary with preparation data.

    This function combines the Wiktionary on'yomi dictionary with preparation data,
    creating a new dictionary with merged and potentially fixed on'yomi information.

    Args:
        wikt_onyomi_dict (dict): The Wiktionary on'yomi dictionary to be merged.
        add_mark_flag (bool): Flag to determine if marks should be added to kanji. Default is True.

    Returns:
        dict: A new dictionary containing merged on'yomi information.
    """
    # Load preparation data
    prpr_full_kanji_map, prpr_kanji_info_dict = load_preparation_data()
    
    # Define appendix marks for different kanji types
    appendix = {"常用": "", "表外": "+", "人名": "*", "異体": ":"} if add_mark_flag else {}
    merged_kanji_dict = {}

    # Iterate through each primary kanji and its info in the preparation data
    for primary_kanji, prpr_kanji_info in prpr_kanji_info_dict.items():
        # Create a new key by joining kanji with their respective marks
        new_key = ''.join([f'{k}{appendix.get(v, "")}' for k, v in prpr_kanji_info['kanji_dict'].items()])
        
        # update prpr_full_kanji_map
        for kanji in prpr_kanji_info['kanji_dict'].keys():
            prpr_full_kanji_map[kanji] = new_key
        
        # merge on'yomi of the original wiktionary data
        merged_onyomi_info = merge_exists_wikt_onyomi_by_prpr_itai_group(prpr_kanji_info['kanji_dict'].keys(), wikt_onyomi_dict)
        # Fix the wiktionary on'yomi information using preparation data if available
        fixed_onyomi_info = fix_by_preparation(merged_onyomi_info, prpr_kanji_info['yomi'])

        # add kun'yomi to the original wiktionary data
        kunyomi_info = get_kunyomi_from_preparation(prpr_kanji_info['yomi'])
        
        merged_kanji_dict[new_key] = {
            "ja": {
                "音読み": fixed_onyomi_info,
                "訓読み": {
                    "訓読み": kunyomi_info
                },
                "語彙": prpr_kanji_info['yomi'].get('語彙', [])
            }
        }

    
    return merged_kanji_dict, prpr_full_kanji_map
        