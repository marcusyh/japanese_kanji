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
    prpr_onyomi_list = list(prpr_onyomi_dict.keys())
    prpr_onyomi_matched_list = []
    new_onyomi_dict_all = {}
    
    # Process both '表内' and '表外' categories
    for category in ['表内', '表外']:
        for reading_type, rt_value in wikt_onyomi_dict_all.items():
            if category not in rt_value:
                continue
            for item in rt_value[category]:
                if 'pron' not in item:
                    continue
                
                # If the pronunciation is in the preparation data
                if item['pron'] in prpr_onyomi_list:
                    prpr_onyomi_matched_list.append(item['pron'])
                    prpr_onyomi_list.remove(item['pron'])
                    
                    # Add to '表内' in the new dictionary
                    if reading_type not in new_onyomi_dict_all:
                        new_onyomi_dict_all[reading_type] = {}
                    if '表内' not in new_onyomi_dict_all[reading_type]:
                        new_onyomi_dict_all[reading_type]['表内'] = []
                    new_onyomi_dict_all[reading_type]['表内'].append(item)
                    item['words_list'] = prpr_onyomi_dict[item['pron']]
                else:
                    # Add to '表外' in the new dictionary
                    if reading_type not in new_onyomi_dict_all:
                        new_onyomi_dict_all[reading_type] = {}
                    if '表外' not in new_onyomi_dict_all[reading_type]:
                        new_onyomi_dict_all[reading_type]['表外'] = []
                    new_onyomi_dict_all[reading_type]['表外'].append(item)
        
        # Break if all preparation data has been processed
        if len(prpr_onyomi_list) == 0:
            break
    
    # Add any remaining preparation data as '慣用音' (customary readings)
    for kanji in prpr_onyomi_list:
        if '慣用音' not in new_onyomi_dict_all:
            new_onyomi_dict_all['慣用音'] = {}
        if '表内' not in new_onyomi_dict_all['慣用音']:
            new_onyomi_dict_all['慣用音']['表内'] = []
        new_onyomi_dict_all['慣用音']['表内'].append({
            'pron': kanji,
            "words_list": prpr_onyomi_dict[kanji]
        })
    
    return new_onyomi_dict_all

    

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
    _, prpr_kanji_info_dict = load_preparation_data()
    
    # Define appendix marks for different kanji types
    appendix = {"常用": "", "表外": "+", "人名": "*", "異体": ":"} if add_mark_flag else {}
    new_onyomi_dict = {}

    # Iterate through each primary kanji and its info in the preparation data
    for primary_kanji, kanji_info in prpr_kanji_info_dict.items():
        # Create a new key by joining kanji with their respective marks
        new_key = ''.join([f'{k}{appendix.get(v, "")}' for k, v in kanji_info['kanji_dict'].items()])
        new_onyomi_info = {}

        # Process each kanji in the kanji_dict
        for kanji in kanji_info['kanji_dict'].keys():
            # Check for different possible keys in the Wiktionary dictionary
            for tail in ['', '1', '2', '3']:
                wikt_key = f'{kanji}{tail}'
                if wikt_key not in wikt_onyomi_dict:
                    continue
                
                # Initialize new_onyomi_info if it's empty
                if not new_onyomi_info:
                    new_onyomi_info = wikt_onyomi_dict[wikt_key]
                    continue
                
                # Skip if the information is identical
                if new_onyomi_info == wikt_onyomi_dict[wikt_key]:
                    continue
                
                # Merge the on'yomi information
                merge_wikt_onyomi_dict(new_onyomi_info, wikt_onyomi_dict[wikt_key])
                
        # Fix the on'yomi information using preparation data if available
        if '音読み' in prpr_kanji_info_dict[primary_kanji]['yomi']:
            fixed_onyomi_info = fix_by_preparation(new_onyomi_info, prpr_kanji_info_dict[primary_kanji]['yomi']['音読み'])
        else:
            fixed_onyomi_info = new_onyomi_info
        
        # Add the merged and fixed on'yomi information to the new dictionary
        new_onyomi_dict[new_key] = fixed_onyomi_info
    
    return new_onyomi_dict
        