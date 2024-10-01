from typing import Dict, List, Any, Tuple, Set
from collections import defaultdict

def get_sorting_keys(kanji_info: Dict[str, Any], include_hyogai: bool) -> tuple:
    """
    Generate sorting keys for a kanji based on its reading information.

    This function processes the kanji's reading information and creates a tuple of sorted readings
    that can be used as a key for sorting kanji. It considers different types of readings (呉音, 漢音, etc.)
    and can optionally include both 表内 (standard) and 表外 (non-standard) readings.

    Args:
        kanji_info (Dict[str, Any]): A dictionary containing the kanji's reading information.
        include_hyogai (bool): If True, include both 表内 and 表外 readings. If False, only include 表内 readings.

    Returns:
        tuple: A tuple of four sorted tuples, where each inner tuple contains sorted readings for a specific reading type
               (呉音, 漢音, 宋唐音, 慣用音). If a reading type has no readings, its corresponding tuple will be empty.

    Example:
        Input:
        kanji_info = {
            '呉音': {
                '表内': [{'pron': 'キョウ'}, {'pron': 'コウ'}],
                '表外': [{'pron': 'ギョウ'}]
            },
            '漢音': {
                '表内': [{'pron': 'コウ'}, {'pron': 'キョウ'}]
            }
        }
        include_hyogai = True

        Output:
        (('キョウ', 'コウ', 'ギョウ'), ('キョウ', 'コウ'), (), ())

    Note:
        The order of reading types is predefined as ['呉音', '漢音', '宋唐音', '慣用音'].
        All four reading types are always included in the final tuple, even if some are empty.
    """
    # Define the order of reading types to be considered
    reading_types_order = ['呉音', '漢音', '宋唐音', '慣用音']
    
    # Determine which categories to include based on the include_hyogai flag
    categories = ['表内', '表外'] if include_hyogai else ['表内']

    # Initialize a dictionary to store sets of readings for each reading type
    reading_sets = {key: set() for key in reading_types_order}
    
    # Iterate through the kanji information
    for reading_type, value in kanji_info.items():
        # Skip reading types not in our predefined order
        if reading_type not in reading_types_order:
            continue
        
        # Process each category (表内 or 表外) in the reading type
        for category, items in value.items():
            # Skip categories we're not interested in
            if category not in categories:
                continue
            
            # Add all pronunciations ('pron') to the set for this reading type
            reading_sets[reading_type].update(item['pron'] for item in items if 'pron' in item)

    # Create a tuple of sorted tuples for each reading type
    # This ensures a consistent order of readings for each type (呉音, 漢音, 慣用音, 宋唐音)
    sorted_readings = tuple(tuple(sorted(reading_sets[key])) for key in reading_types_order)
    
    # Return the sorted readings
    # This tuple can be used as a key for sorting kanji based on their readings
    return sorted_readings


def sort_kanji(kanji_data: Dict[str, Any], include_hyogai: bool = False) -> List[str]:
    """
    Sort kanji based on their reading information.

    This function sorts the kanji keys in the input dictionary based on their reading information,
    using the get_sorting_keys function to generate sorting keys for each kanji.

    Args:
        kanji_data (Dict[str, Any]): A dictionary where keys are kanji and values are their reading information.
        include_hyogai (bool, optional): If True, include both 表内 and 表外 readings in sorting. Defaults to False.

    Returns:
        List[str]: A list of kanji sorted based on their reading information.

    Example:
        Output:
        ['亜', '唖', '娃', '阿', '哀', '愛', '挨', '姶', '逢', '葵']
    """
    return sorted(kanji_data.keys(), key=lambda k: get_sorting_keys(kanji_data[k], include_hyogai))


def sort_and_merge_kanji(kanji_data: Dict[str, Any], include_hyogai: bool = False) -> Dict[Tuple[Tuple[str, ...], ...], List[str]]:
    """
    Sort and merge kanji based on their reading information.

    This function groups kanji with similar readings together and sorts these groups.
    It prioritizes grouping based on 呉音 (go-on), 漢音 (kan-on), 慣用音 (kan'yō-on),
    and 宋唐音 (sō-tō-on) readings in that order.

    Args:
        kanji_data (Dict[str, Any]): A dictionary where keys are kanji and values are their reading information.
        include_hyogai (bool, optional): If True, include both 表内 and 表外 readings in sorting. Defaults to False.

    Returns:
        Dict[Tuple[Tuple[str, ...], ...], List[str]]: A dictionary where:
            - Keys are tuples of tuples, each inner tuple containing strings of readings used for sorting (go-on, kan-on, kan'yō-on, sō-tō-on)
            - Values are lists of kanji with similar readings based on the sorting key

    Example:
        Output:
        {
            (('カ',), ('カ',), (), ()): ['火', '花'],
            (('ニチ',), ('ジツ',), (), ()): ['日', '実'],
            (('スイ',), ('スイ',), (), ()): ['水', '垂'],
            ...
        }
    """
    kanji_groups = defaultdict(list)
    
    reading_types = ['呉音', '漢音', '慣用音', '宋唐音']
    for kanji, info in kanji_data.items():
        if not info:
            continue

        # Get sorting keys for the current kanji
        go, kan, kanyou, soto = get_sorting_keys(info, include_hyogai)
        
        # Determine the grouping key based on available readings
        # Priority: 呉音/漢音 > 慣用音 > 宋唐音
        if go or kan:
            key = (go, kan, (), ())
        elif kanyou:
            key = ((), (), kanyou, ())
        elif soto:
            key = ((), (), (), soto)
        else:
            key = ((), (), (), ())
        
        kanji_groups[key].append(kanji)
    
    return kanji_groups
        


def merge_kanji_info(kanji_list: List[str], info: Dict[str, Any], include_hyogai: bool = False) -> Dict[str, List[str]]:
    """
    Merge information for a list of kanji characters.

    This function combines the reading information for multiple kanji characters,
    organizing them by reading type and pronunciation.

    Args:
        kanji_list (List[str]): A list of kanji characters to process.
        info (Dict[str, Any]): A dictionary containing detailed information for each kanji.
        include_hyogai (bool, optional): Whether to include 表外 (hyōgai) readings. Defaults to False.

    Returns:
        Dict[str, List[str]]: A dictionary with merged kanji information, where keys are reading types
        and values are sets of pronunciations.

    Example:
        Input:
        kanji_list = ['日', '本']
        info = {
            '日': {
                '呉音': {'表内': {'pron': 'アイウ', 'pron_old': 'エオカ'}},
                '漢音': {'表内': {'pron': 'アイウ', 'pron_old': 'キクケ'}},
                '慣用音': {'表内': {'pron': 'アイウ', 'pron_old': 'コサシ'}},
                '宋唐音': {'表内': {'pron': 'スセソ', 'pron_old': 'タチツ'}},
            },
            '本': {
                '呉音': {'表内': {'pron': 'アイウ', 'pron_old': 'テトナ'}},
                '漢音': {'表内': {'pron': 'アイウ', 'pron_old': 'ニヌネ'}},
                '慣用音': {'表内': {'pron': 'アイウ', 'pron_old': 'ノハヒ'}},
            }
        }
        include_hyogai = False

        Output:
        {
            '呉音_pron': {'アイウ'},
            '呉音pron_old': {'エオカ', 'テトナ'},
            '漢音_pron': {'アイウ'},
            '漢音pron_old': {'キクケ', 'ニヌネ'},
            '慣用音_pron': {'アイウ'},
            '慣用音pron_old': {'コサシ', 'ノハヒ'},
            '宋唐音_pron': {'スセソ(日)'},
            '宋唐音pron_old': {'タチツ'}
        }
    """
    # List of reading types that don't require kanji specification in output
    group_key_list = ['呉音', '漢音', '慣用音']
    
    merged = {
        "漢字": kanji_list
    }

    for kanji in kanji_list:
        for reading_type, v in info[kanji].items():
            for category, items in v.items():
                # Skip 表外 (hyōgai) readings if not included
                if category == '表外' and not include_hyogai:
                    continue
                for item in items:
                    for pron, yomi in item.items():
                        # Determine the key based on whether it's a current or old pronunciation
                        key = reading_type if pron == 'pron' else f'{reading_type}_old'
                        
                        # Initialize set for this key if it doesn't exist
                        if key not in merged:
                            merged[key] = {}
                        
                        if yomi not in merged[key]:
                            merged[key][yomi] = []
                        merged[key][yomi].append(kanji)
                        
    for reading_type, item in merged.items():
        if reading_type == '漢字':
            continue
        # Add pronunciation to set, with kanji specification for certain reading types
        if reading_type.endswith('_old') or reading_type in group_key_list:
            merged[reading_type] = list(sorted(item.keys()))
        else:
            sorted_yomis = list(sorted(item.items(), key=lambda x: x[0]))
            new_yomis = []
            for yomi, kanji_list in sorted_yomis:
                new_yomis.append(f'{yomi}({"、".join(kanji_list)})')
            merged[reading_type] = new_yomis
                        
    return merged


def create_merged_dict(kanji_group: Dict[str, List[str]], info: Dict[str, Any], include_hyogai: bool = False) -> Dict[str, Dict[str, Set[str]]]:
    """
    Create a merged dictionary of kanji information for each group of kanji.

    This function processes each group of kanji characters, merging their
    information using the merge_kanji_info function.

    Args:
        kanji_group (Dict[str, List[str]]): A dictionary where keys are group identifiers
                                            and values are lists of kanji characters.
        info (Dict[str, Any]): A dictionary containing detailed information for each kanji.
        include_hyogai (bool, optional): Whether to include 表外 (hyōgai) readings. 
                                         Defaults to False.

    Returns:
        Dict[str, Dict[str, Set[str]]]: A dictionary where:
            - Keys are the original group identifiers.
            - Values are dictionaries returned by merge_kanji_info, containing
              merged information for all kanji in that group.
    """
    new_kanji_group = {}
    for key, kanji_list in kanji_group.items():
        # Merge information for all kanji in the current group
        merged = merge_kanji_info(kanji_list, info, include_hyogai)
        # Store the merged information under the original group key
        new_kanji_group[key] = merged
    
    return new_kanji_group


def convert_to_merged_dict(info: Dict[str, Any], include_hyogai: bool = False) -> Dict[str, Dict[str, Set[str]]]:
    """
    Convert the input dictionary to a merged dictionary.

    This function processes the input dictionary and converts it into a new dictionary
    where each key is a group identifier and the value is a dictionary containing merged
    information for all kanji in that group.

    Args:
        info (Dict[str, Any]): The input dictionary containing detailed information for each kanji.
        include_hyogai (bool, optional): Whether to include 表外 (hyōgai) readings. Defaults to False.

    Returns:
        Dict[str, Dict[str, Set[str]]]: A dictionary where:
            - Keys are the original group identifiers.
            - Values are dictionaries returned by merge_kanji_info, containing
              merged information for all kanji in that group.

    Example:
        Input:
        {
            '亨': {
                '呉音': {
                    '表内': [
                        {'pron': 'キョウ', 'old_pron1': 'キャゥ'},
                        {'pron': 'コウ', 'old_pron1': 'カゥ'},
                        {'pron': 'ヒョウ', 'old_pron1': 'ヒャゥ'}
                    ],
                    '表外': [
                        {'pron': 'XXX', 'old_pron1': 'YYY'},
                        {'pron': 'ZZZ'},
                    ]
                },
                '漢音': {
                    '表内': [
                        {'pron': 'コウ', 'old_pron1': 'カゥ'},
                        {'pron': 'キョウ', 'old_pron1': 'キャゥ'},
                        {'pron': 'ホウ', 'old_pron1': 'ハゥ'}
                    ],
                    '表外': [
                        {'pron': 'XXX', 'old_pron1': 'YYY'},
                        {'pron': 'ZZZ'},
                    ]
                },
                '慣用音': {
                    ...
                }
            },
            ...
        }
        Sub-keys of input: ['呉音', '漢音', '慣用音', '宋唐音', '古音']

    Note:
        The output structure will depend on the input data and the merge_kanji_info function's implementation.
    """ 
    kanji_group = sort_and_merge_kanji(info, include_hyogai)
    merged_dict = create_merged_dict(kanji_group, info, include_hyogai)
    return sorted(merged_dict.items(), key=lambda x: x[0])