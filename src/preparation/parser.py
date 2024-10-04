from preparation.jouyou import load_jouyou
from preparation.jinmei import load_jinmei
from preparation.hyougai import load_hyougai
from preparation.itai import load_itai
from util_kana import check_katakana_hirakana


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
        if type(words) == list:
            print(kana, words)
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

    return all_kanji_mapping, kanji_info_dict
