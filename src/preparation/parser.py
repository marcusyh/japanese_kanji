from preparation.jouyou import load_jouyou
from preparation.jinmei import load_jinmei
from preparation.hyougai import load_hyougai
from preparation.itai import load_itai
from util_kana import check_katakana_hirakana
from collections import Counter

def append_yomi(yomi_dict, kanji_info, source_name, raw_kanji):
    """
    Append yomi (reading) information to the kanji dictionary.

    Args:
        yomi_dict (dict): The dictionary to store yomi information.
        kanji_info (dict): The yomi information for the kanji.
        source_name (str): The name of the source (e.g., "常用", "表外", etc.).
        raw_kanji (str): The original kanji string, potentially containing multiple forms.

    This function processes the yomi information and categorizes it as either 'kunyomi' (訓読み) or 'onyomi' (音読み).
    It also handles error cases and appends the processed information to the yomi_dict.
    """
    for kana, words in kanji_info.items():
        if type(words) == list and kana == '':
            # some special words pronunciation is not categorized as kunyomi or onyomi
            if '語彙' not in yomi_dict:
                yomi_dict['語彙'] = []
            yomi_dict['語彙'].extend(words)
            continue
        # Clean the pronunciation and create a list of associated words
        pron = kana.strip()
        word_list = [word.strip() for word in words.split(' ')] if words else []

        # Check if the pronunciation is hiragana or katakana
        hira_exists, kata_exists = check_katakana_hirakana(pron)

        # Error handling for invalid pronunciations
        if hira_exists and kata_exists or not hira_exists and not kata_exists:
            print(f"Error found: {source_name}, {raw_kanji}, {kanji_info}, {kana}, {words}")
            continue

        # Determine if it's kunyomi (hiragana) or onyomi (katakana)
        yomi_key = '訓読み' if hira_exists else '音読み'

        # Initialize the yomi category if it doesn't exist
        if yomi_key not in yomi_dict:
            yomi_dict[yomi_key] = {}

        # Append the pronunciation and associated words to the appropriate category
        yomi_dict[yomi_key].update({pron: word_list})
        

def find_common_stem(target, readings):
    """
    Find the longest common stem among the target reading and other readings.

    Args:
        target (str): The target reading to find a stem for.
        readings (list): A list of all readings to compare against.

    Returns:
        str: The longest common stem, or the full target if no common stem is found.

    This function works as follows:
    1. Start with the full length of the target reading.
    2. Iteratively reduce the length, checking for common stems.
    3. For each potential stem, count how many readings start with it.
    4. If more than one reading starts with the stem, it's considered common.
    5. Return the longest common stem found, or the full target if none is found.
    """
    max_length = len(target)
    for length in range(max_length, 0, -1):
        # Get a potential stem by slicing the target
        stem = target[:length]
        # Count how many readings start with this stem
        # If more than one, it's a common stem
        if sum(1 for r in readings if r.startswith(stem)) > 1:
            return stem
    # If no common stem is found, return the full target
    return target


def find_kanji_reading(kanji, key, examples):
    """
    Find the most probable reading of a kanji based on examples.

    Args:
        kanji (str): The kanji character.
        key (str): The full reading (usually in hiragana).
        examples (list): A list of example words containing the kanji.

    Returns:
        str: The most probable reading of the kanji.
    """
    readings = []
    for example in examples:
        if kanji not in example:
            continue
        
        kanji_index = example.index(kanji)
        if kanji_index == len(example) - 1:
            readings.append(key)
            continue

        sub_container = example[kanji_index+1:]
        
        # Find the maximum common substring at the start of sub_container and end of key
        max_common = ""
        for i in range(min(len(sub_container), len(key)), 0, -1):
            if sub_container.startswith(key[-i:]):
                max_common = key[-i:]
                break
        
        # Remove the common part from key
        new_key = key[:-len(max_common)]
        
        if new_key != '':
            readings.append(new_key)
    
    # Count occurrences of each reading and return the most common one
    key = Counter(readings).most_common(1)[0][0] if readings else key
    
    return key

def merge_kunyomi(kanji, kunyomi_ori_dict):
    if not kunyomi_ori_dict:
        return {}
    if len(kunyomi_ori_dict) == 1:
        k, v = list(kunyomi_ori_dict.items())[0]
        return {k: {k: v}}

    merged = {}
    for reading, examples in kunyomi_ori_dict.items():
        #stem = find_common_stem(reading, list(kunyomi_ori_dict.keys()))
        stem = find_kanji_reading(kanji, reading, examples)
        if stem not in merged:
            merged[stem] = {}
        merged[stem][reading] = examples
        
    """
    for stem, readings in merged.items():
        merged_words_list = [[reading] + examples for reading, examples in readings.items()]
        merged[stem] = merged_words_list
    """ 
    return merged


def load_preparation_data(
        jouyou=True,
        jinmei=True,
        hyougai=True,
        itai=True,
        with_tag=True,
        data_root_dir='../data/preparation/'
    ):
    """
    This function loads kanji data from different sources (jouyou, jinmei, hyougai, and itai),
    processes the data, and returns two dictionaries containing kanji information.

    Args:
        jouyou (bool): Whether to load jouyou kanji data. Default is True.
        jinmei (bool): Whether to load jinmei kanji data. Default is True.
        hyougai (bool): Whether to load hyougai kanji data. Default is True.
        itai (bool): Whether to load itai kanji data. Default is True.
        with_tag (bool): Whether to include tags in the output. Default is True.
        data_root_dir (str): The root directory for data files. Default is '../data/preparation/'.

    Returns:
        tuple: A tuple containing two dictionaries:
            - all_kanji_mapping (dict): A mapping of individual kanji to their representative kanji.
            - kanji_info_dict (dict): Detailed information for each kanji group.

    Note:
        The kanji with the smallest Unicode value in each itai kanji group is treated as the key.
        All kanji in the itai kanji group are included in the value list.

    Output example:
    {
        '亜': {
            "kanji_dict": {
                '亜': '常用',
                '亞': '常用',
            },
            'yomi': {
                "音読み": {
                    'ア': ['亜流', '亜麻', '亜熱帯']
                }
            }
        },
        '哀': {
            'kanji_dict': {
                '哀': '常用',
            },
            'yomi': {
                "音読み": {
                    'アイ': ['哀愁', '哀願', '悲哀'],
                },
                "訓読み": {
                    'あわれ': ['哀れ', '哀れな話', '哀れがる'],
                    'あわれむ': ['哀れむ', '哀れみ']
                }
            }
        }
        ...
    }
    """
    # Dictionary to store the mapping between individual kanji and their representative kanji
    all_kanji_mapping = {}
    # Dictionary to store detailed information for each kanji group
    kanji_info_dict = {}

    # Load data from different sources based on the function parameters
    jouyou = load_jouyou(data_root_dir) if jouyou else {}
    hyougai = load_hyougai(data_root_dir) if hyougai else {}
    jinmei = load_jinmei(data_root_dir) if jinmei else {}
    itai = load_itai(data_root_dir) if itai else {}

    # Process and merge data from all sources
    for source, source_name in zip([jouyou, hyougai, jinmei, itai], ["常用", "表外", "人名", "異体"]):
        for raw_kanji, kanji_info in source.items():
            if raw_kanji.strip().strip('/') == '':
                continue

            # split to kanji list, then get the matched and mismatched kanji in all_kanji_dict
            kanji_list = [kanji.strip() for kanji in raw_kanji.split('/')]
            matched = [kanji for kanji in kanji_list if kanji in all_kanji_mapping]
            mismatched = {kanji: source_name for kanji in list(set(kanji_list) - set(matched))}
            
            # Determine the representative kanji for this group
            kanji_info_key = all_kanji_mapping[matched[0]] if matched else kanji_list[0]

            # Create a new entry in kanji_info_dict if this is a new kanji group
            if not matched:
                kanji_info_dict[kanji_info_key] = {
                    "kanji_dict": {},
                    "yomi": {},
                }
            kanji_info_dict[kanji_info_key]['kanji_dict'].update(mismatched)
            
            # Process and append yomi information
            yomi_dict = kanji_info_dict[kanji_info_key]['yomi']
            append_yomi(yomi_dict, kanji_info, source_name, raw_kanji)

            # Update the mapping for all kanji in this group
            all_kanji_mapping.update({kanji: kanji_info_key for kanji in kanji_list})
            

    for kanji, value in kanji_info_dict.items():
        if '訓読み' in value['yomi']:
            new_kunyomi = merge_kunyomi(kanji, value['yomi']['訓読み'])
            value['yomi']['訓読み'] = new_kunyomi

    return all_kanji_mapping, kanji_info_dict
