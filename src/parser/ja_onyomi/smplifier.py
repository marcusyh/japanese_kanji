from typing import Dict, List, Any, Tuple, Set
from collections import defaultdict


def simplify_onyomi(kanji_info: Dict[str, Any], include_hyogai: bool = False) -> Dict[str, Any]:
    """
    Simplifies the onyomi (音読み) information for a kanji.

    This function takes a complex dictionary of kanji reading information and simplifies it
    into a more manageable structure. It consolidates readings across different categories
    and types into sets, making it easier to process and compare kanji readings.

    Args:
        kanji_info (Dict[str, Any]): A dictionary containing detailed onyomi information for a kanji.
        include_hyogai (bool, optional): If True, include both 表内 and 表外 readings. Defaults to False.

    Returns:
        Dict[str, Any]: A simplified dictionary of kanji reading information.

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
        {
            'pron': {'キョウ', 'コウ', 'ギョウ'}
        }

        If include_hyogai = False:
        {
            'pron': {'キョウ', 'コウ'}
        }
    """
    # Initialize the new simplified kanji info dictionary
    new_kanji_info = {'pron': set(), 'old': set()}
    
    for categories in kanji_info.values():
        for category, items in categories.items():
            # Skip 表外 readings if include_hyogai is False
            if not include_hyogai and category == '表外':
                continue
            
            for item in items:
                for pron_key, pron_value in item.items():
                    # Simplify the pronunciation key to either 'pron' or 'old'
                    simplified_key = 'pron' if pron_key == 'pron' else 'old'
                    new_kanji_info[simplified_key].add(pron_value)
    
    # Remove empty sets
    return {k: v for k, v in new_kanji_info.items() if v}


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


def group_kanji(kanji_data: Dict[str, Any], include_hyogai: bool = False) -> Dict[Tuple[Tuple[str, ...], ...], List[str]]:
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
    
    reading_types = ['呉音', '漢音', '宋唐音', '慣用音']
    for kanji, info in kanji_data.items():
        if not info:
            continue

        # Get sorting keys for the current kanji
        go, kan, soto, kanyou = get_sorting_keys(info, include_hyogai)
        
        # Determine the grouping key based on available readings
        # Priority: 呉音/漢音 > 慣用音 > 宋唐音
        if go:
            key = (go, kan, (), ())
            sort_key = (go, kan)
        elif kan:
            key = ((), kan, (), ())
            sort_key = (kan, ())
        elif soto:
            key = ((), (), soto, ())
            sort_key = (soto,())
        elif kanyou:
            key = ((), (), (), kanyou)
            sort_key = (kanyou, ())
        else:
            key = ((), (), (), ())
            sort_key = ((), ())

        if key not in kanji_groups:
            kanji_groups[key] = [sort_key, [kanji]]
        else:
            kanji_groups[key][1].append(kanji)
    
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
    group_key_list = ['呉音', '漢音']
    
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
        if reading_type.endswith('_old') or reading_type in group_key_list or len(merged['漢字']) == 1:
            merged[reading_type] = list(sorted(item.keys()))
        else:
            sorted_yomis = list(sorted(item.items(), key=lambda x: x[0]))
            new_yomis = []
            for yomi, kanji_list in sorted_yomis:
                new_yomis.append(f'{yomi}({"、".join(kanji_list)})')
            merged[reading_type] = new_yomis
                        
    return merged


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
    kanji_group = group_kanji(info, include_hyogai)

    merged_group= {}
    for group_key, group_value in kanji_group.items():

        sort_key, kanji_list = group_value
        # Merge information for all kanji in the current group
        merged = merge_kanji_info(kanji_list, info, include_hyogai)
        # Store the merged information under the original group key
        merged_group[group_key] = [sort_key, merged]
    
    # Convert the merged_group dictionary to a sorted list of tuples (group_key, merged_info)
    sorted_group = sorted(merged_group.items(), key=lambda x: x[1][0])

    return [x[1][1] for x in sorted_group]
