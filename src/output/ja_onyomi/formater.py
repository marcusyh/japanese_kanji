from typing import Dict, List, Any, Tuple, Set, Union
import copy
from collections import defaultdict

def get_sorting_keys(kanji_info: Dict[str, Any], merge_hyogai: bool) -> tuple:
    """
    Generate sorting keys for a kanji based on its reading information.

    This function processes the kanji's reading information and creates a tuple of sorted readings
    that can be used as a key for sorting kanji. It considers different types of readings (呉音, 漢音, etc.)
    and can optionally include both 表内 (standard) and 表外 (non-standard) readings.

    Args:
        kanji_info (Dict[str, Any]): A dictionary containing the kanji's reading information.
        merge_hyogai (bool): If True, merge 表外 (hyōgai) readings. If False, only include 表内 readings.

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
    categories = ['表内', '表外'] if merge_hyogai else ['表内']

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


def sort_kanji(kanji_data: Dict[str, Any], merge_hyogai: bool = False) -> List[str]:
    """
    Sort kanji based on their reading information.

    This function sorts the kanji keys in the input dictionary based on their reading information,
    using the get_sorting_keys function to generate sorting keys for each kanji.

    Args:
        kanji_data (Dict[str, Any]): A dictionary where keys are kanji and values are their reading information.
        merge_hyogai (bool, optional): If True, merge 表外 (hyōgai) readings. Defaults to False.

    Returns:
        List[str]: A list of kanji sorted based on their reading information.

    Example:
        Output:
        ['亜', '唖', '娃', '阿', '哀', '愛', '挨', '姶', '逢', '葵']
    """
    return sorted(kanji_data.keys(), key=lambda k: get_sorting_keys(kanji_data[k], merge_hyogai))


def group_kanji(
        kanji_data: Dict[str, Any],
        merge_hyogai: bool = False
    ) -> Dict[Tuple[Tuple[str, ...], ...], List[str]]:
    """
    Sort and merge kanji based on their reading information.

    This function groups kanji with similar readings together and sorts these groups.
    It prioritizes grouping based on 呉音 (go-on), 漢音 (kan-on), 慣用音 (kan'yō-on),
    and 宋唐音 (sō-tō-on) readings in that order.

    Args:
        kanji_data (Dict[str, Any]): A dictionary where keys are kanji and values are their reading information.
        merge_hyogai (bool, optional): If True, merge 表外 (hyōgai) readings. Defaults to False.

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
        go, kan, soto, kanyou = get_sorting_keys(info, merge_hyogai)
        
        # Determine the grouping key based on available readings
        # Priority: 呉音/漢音 > 慣用音 > 宋唐音
        if go:
            group_key = (go, kan, (), ())
            sort_key = (go, kan)
        elif kan:
            group_key = ((), kan, (), ())
            sort_key = (kan, ())
        elif soto:
            group_key = ((), (), soto, ())
            sort_key = (soto,())
        elif kanyou:
            group_key = ((), (), (), kanyou)
            sort_key = (kanyou, ())
        else:
            group_key = ((), (), (), ())
            sort_key = ((), ())

        group_key = (go, kan, soto, kanyou)
        if group_key not in kanji_groups:
            kanji_groups[group_key] = [sort_key, [kanji]]
        else:
            kanji_groups[group_key][1].append(kanji)
    
    return kanji_groups
        


def merge_kanji_info(
        kanji_list: List[str], 
        info: Dict[str, Any], 
        merge_hyogai: bool = False,
        show_hyogai: bool = False
    ) -> Tuple[Dict[str, List[str]], Set[str]]:
    """
    Merge information for a list of kanji characters.

    This function combines the reading information for multiple kanji characters,
    organizing them by reading type and pronunciation.

    Args:
        kanji_list (List[str]): A list of kanji characters to process.
        info (Dict[str, Any]): A dictionary containing detailed information for each kanji.
        merge_hyogai (bool, optional): Whether to merge 表外 (hyōgai) readings. Defaults to False.

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
            '呉音': {'アイウ, xxxx'},
            '呉音_表外': {'xxxx'},
            '呉音_old': {'エオカ', 'テトナ'},
            '漢音': {'アイウ'},
            '漢音_old': {'キクケ', 'ニヌネ'},
            '慣用音': {'アイウ'},
            '慣用音_old': {'コサシ', 'ノハヒ'},
            '宋唐音': {'スセソ(日)'},
            '宋唐音_old': {'タチツ'}
        }
    """
    # List of reading types that don't require kanji specification in output
    merged = {
        "漢字": kanji_list,
    }
    all_prons = set()

    def add_to_merged(key, yomi, kanji):
        # Initialize set for this key if it doesn't exist
        if key not in merged:
            merged[key] = {}
        if yomi not in merged[key]:
            merged[key][yomi] = []
        merged[key][yomi].append(kanji)
        
    def add_pron(category, pron, reading_type, yomi, kanji):
        if pron == 'pron':
            key = reading_type if category == '表内' else f'{reading_type}_表外'
            if category == '表内':
                all_prons.add(yomi)
        else:
            key = f'{reading_type}_old' if category == '表内' else f'{reading_type}_表外_old'
        add_to_merged(key, yomi, kanji)
        
    # category: 表内, 表外
    # pron: pron, pron_old
    # reading_type: 呉音, 漢音, 宋唐音, 慣用音
    # yomi: アイウ, エオカ, キクケ, コサシ, スセソ, タチツ, テトナ, ニヌネ, ノハヒ 
    # kanji: 亜, 唖, 娃, 阿, 哀, 愛, 挨, 姶, 逢, 葵
    def add_prons(category, pron, reading_type, yomi, kanji):
        if merge_hyogai:
            add_pron('表内', pron, reading_type, yomi, kanji)
        elif show_hyogai:
            if pron != 'pron':
                category = '表内'
            add_pron(category, pron, reading_type, yomi, kanji)
        else:
            add_pron(category, pron, reading_type, yomi, kanji)

    group_key_list = ['呉音', '漢音']
    for kanji in kanji_list:
        for reading_type, v in info[kanji].items():
            for category, items in v.items():
                for item in items:
                    for pron, yomi in item.items():
                        add_prons(category, pron, reading_type, yomi, kanji)

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
                        
    return merged, all_prons


def merge_onyomi_groups(
        kanji_groups: Dict[str, Any],
        info: Dict[str, Any],
        merge_hyogai: bool = False,
        show_hyogai: bool = False,
    ) -> Dict[str, List[Union[str, Set[str], Dict[str, Any]]]]:
    """
    Merge and process information for kanji groups.

    This function takes kanji groups and their detailed information, merges the information
    for each group, and returns a new dictionary with processed data for each group.

    Args:
        kanji_groups (Dict[str, Any]): A dictionary of kanji groups, where each value is a tuple
                                       containing a sort key and a list of kanji.
        info (Dict[str, Any]): A dictionary containing detailed information for each kanji.
        include_hyogai (bool, optional): Whether to include 表外 (hyōgai) readings. Defaults to False.

    Returns:
        Dict[str, List[Union[str, Set[str], Dict[str, Any]]]]: A dictionary where:
            - Keys are the original group identifiers.
            - Values are lists containing:
                1. The sort key for the group
                2. A set of all pronunciations for the group
                3. A dictionary of merged information for all kanji in the group

    Example:
        Input kanji_groups:
        {
            'group1': ('sort_key1', ['亨', '享']),
            'group2': ('sort_key2', ['亭', '停'])
        }

        Output:
        {
            'group1': ['sort_key1', {'キョウ', 'コウ', ...}, {...}],
            'group2': ['sort_key2', {'テイ', 'チョウ', ...}, {...}]
        }

    Note:
        The structure of the merged information dictionary (third element in the value list)
        depends on the implementation of the merge_kanji_info function.
    """ 
    merged_groups = {}
    for group_key, group_value in kanji_groups.items():
        sort_key, kanji_list = group_value
        # Merge information for all kanji in the current group
        merged, all_prons = merge_kanji_info(kanji_list, info, merge_hyogai, show_hyogai)
        # Store the merged information under the original group key
        merged_groups[group_key] = [sort_key, all_prons, merged]
        
    return merged_groups



def expand_and_sort_groups(groups: Dict[Tuple[Tuple[str, ...], ...], Any], duplicate_by_all: bool = False) -> List[Dict[str, Any]]:
    """
    Expand groups by pronunciations and sort them.

    This function processes the input groups, expands them based on pronunciations,
    and sorts them first by pronunciation and then by their original index.

    Args:
        groups (List[Dict[str, Any]]): A list of dictionaries, where each dictionary
            contains a group of kanji information including pronunciations.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, sorted by pronunciation and original index,
        with each pronunciation having its own entry.
    """
    # Create new groups, expanding each group for every pronunciation it has
    new_groups = []
    for index, sorted_value in enumerate(sorted(groups.items(), key=lambda x: x[1][0]), start=1):
        group_key, group_wrapper = sorted_value
        sort_key, all_prons, merged_group = group_wrapper
        # Add index and sort_key to the group information
        merged_group.update({
            "index": index,
            "sort_key": sort_key,
        })
        
        # if not duplicate_by_all, just append the group
        if not duplicate_by_all:
            new_groups.append(merged_group)
            continue
        
        # Create a new entry for each pronunciation in the group
        for pron in sorted(all_prons):
            output_group = copy.deepcopy(merged_group)
            new_groups.append({
                **output_group,
                "音序": pron,
                "main_row_flag": False
            })
    
    if not duplicate_by_all:
        return sorted(new_groups, key=lambda x: x['index'])

    # Sort the new groups first by pronunciation, then by original index
    sorted_rows = sorted(new_groups, key=lambda x: (x['音序'], x['index']))
    
    # add main_row flag to show which row is the original row among the duplicate rows
    prev_row = None
    for row in sorted_rows:
        current_row = row['index']
        if prev_row == None or current_row == prev_row + 1:
            row['main_row_flag'] = True
            prev_row = current_row
        
    return sorted_rows

        


def generate_onyomi_rows(
        info: Dict[str, Any],
        merge_hyogai: bool = False,
        show_hyogai: bool = False,
        show_duplicated: bool = False,
    ) -> List[Dict[str, Any]]:
    """
    This function processes the input dictionary, groups kanji, merges information for each group,
    and then expands and sorts the groups based on pronunciations.

    Args:
        info (Dict[str, Any]): The input dictionary containing detailed information for each kanji.
        merge_hyogai (bool, optional): Whether to merge 表外 (hyōgai) readings. Defaults to False.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents
        an expanded and sorted group entry. Each entry contains merged information
        for a group of kanji, including pronunciations and other relevant data.
        
    Elements of each row of the output:
        - 'onyomi': 'アイウ'
        - 'index': 1234
        - 'sort_key': ('アイウ',)
        - 'merged': Dict[str, Any]
        - '呉音': {'アイウ'},
        - '呉音_old': {'エオカ', 'テトナ'},
        - '漢音': {'アイウ'},
        - '漢音_old': {'キクケ', 'ニヌネ'},
        - '慣用音': {'アイウ'},
        - '慣用音_old': {'コサシ', 'ノハヒ'},
        - '宋唐音': {'スセソ(日)'},
        - '宋唐音_old': {'タチツ'}
    """ 
    # Group kanji into groups
    kanji_groups = group_kanji(info, merge_hyogai)
    
    # Merge information for each group
    merged_groups = merge_onyomi_groups(kanji_groups, info, merge_hyogai, show_hyogai)
    
    # Expand and sort the groups based on pronunciations and original order
    return expand_and_sort_groups(merged_groups, show_duplicated)