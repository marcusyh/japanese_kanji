import re

# Dictionary of all special cases where each key is a kanji and the value is the modified 'element'
onyomi_special_cases = {
    '加': [
        '音読み',
        ['[[漢音]]: [[カ]]']
    ],
    '法': [
        '音読み',
        ['[[呉音]]: [[ホウ]]、[[ホフ]]、[[ホッ]]'],
        ['[[漢音]]: [[ホウ]]、[[ハフ]]、[[ハッ]]']
    ],
    '合': [
        '音読み',
        [' [[呉音]] : [[ゴウ]]、[[ガフ]]、[[ガッ]]'],
        [' [[漢音]] : [[コウ]]、[[カフ]]、[[カッ]]']
    ],
    '月': [
        '音読み',
        [' [[呉音]] : [[ハク]]'],
        [' [[漢音]] : [[ハク]]']
    ],
    '寝': [
        '音読み',
        [' [[呉音]] : [[シン]]([[シム]])'],
        [' [[漢音]] : [[シン]]([[シム]])']
    ],
    '弁': [
        '音読み',
        [' [[呉音]] : [[ベン]]'],
        [' [[漢音]] : [[ヘン]]、[[ハン]]']
    ],
    '終': [
        '音読み',
        [' [[呉音]] : [[シュ]]'],
        [' [[漢音]] : [[シュウ]]([[シュゥ]])']
    ],
    '畠': [
        '音読み',
        [' [[呉音]] : [[ガチ]]（グヮチ）、[[ガツ]]（グヮツ）'],
        [' [[漢音]] : [[ゲツ]]（グヱツ）'],
        [' [[慣用音]] : [[ガツ]]（グヮツ）']
    ],
    '分': [
        '音読み',
        [' [[呉音]] : [[ブン]]、[[フン]]'],
        [' [[漢音]] : [[フン]]、[[プン]]'],
        [' [[宋音]] : [[フン]]'],
        [' [[慣用音]] : [[ブ]]']
    ],
    '灯': [
        ' 音読み',
        [' [[呉音]] : [[チョウ]] ([[チャゥ]]）（表外）'],
        [' [[漢音]] : [[テイ]] ([[ティ]]）（表外）'],
        [' [[慣用音]] : [[チン]]（表外）、[[トン]]（表外）']
    ],
    '央': [
        ' 音読み',
        [' [[呉音]]: [[オウ]] 、[[ヨウ]]（常用外）'],
        [' [[漢音]]: [[ヨウ]]（常用外）、[[エイ]]（常用外）']
    ],
    '貼': [
        ' 音読み',
        [' [[呉音]] : [[チョウ]]([[テフ]])'],
        [' [[漢音]] : [[チョウ]]([[テフ]])'],
        [' [[慣用音]] : [[テン]](表外)']
    ],
    '芸': [
        ' 音読み',
        [' [[呉音]] : [[ゲ]]、[[ウン]]'],
        [' [[漢音]] : [[ゲイ]]、[[ウン]]'],
    ],
    '禅': [
        ' 音読み',
        [' [[呉音]] : [[ゼン]]'],
        [' [[漢音]] : [[セン]](表外)']
    ],
    '作': [
        ' 音読み',
        [' [[呉音]] : [[サク]]、[[サ]]、[[サッ]] '],
        [' [[漢音]] : [[サク]]、[[サ]]、[[サッ]] '],
    ],
    '十': [
        ' 音読み',
        [' [[呉音]] : [[ジュウ]]（[[ジフ]]）、[[ジッ]]'],
        [' [[漢音]] : [[シュウ]]（[[シフ]]）（表外）'],
        [' [[慣用音]] :[[ジュッ]]'],
    ],
    '入':[
        " 音読み :",
        [" [[呉音]] : [[ニュウ]]（ニフ）"],
        [" [[漢音]] : [[ジュウ]]（ジフ）"],
        [" [[慣用音]] : [[ジュ]]"]
    ], 
    '甲':[
        " 音読み",
        [" [[呉音]] : [[キョウ]]"],
        [" [[漢音]] : [[コウ]]"],
        [" [[慣用音]] : [[カン]]"]
    ],
    '南': [
        '音読み',
        ['[[呉音]] : [[ナン]]、[[ナ]]'],
        ['[[漢音]] : [[ダン]]']
    ],
    '怜': [
        '音読み',
        ['[[呉音]] : [[リョウ]]([[リャゥ]])'],
        ['[[漢音]] : [[レイ]]([[レィ]])、[[レン]]']
    ],
    '耗': [
        '音読み',
        ['[[呉音]] : [[コウ]]([[カウ]])'],
        ['[[漢音]] : [[コウ]]([[カウ]])'],
        ['[[慣用音]] : [[モウ]]']
    ],
    '栗': [
        '音読み',
        ['[[呉音]] : [[リチ]]'],
        ['[[漢音]] : [[リツ]]'],
        ['[[唐音]] : リツ'],
        ['[[慣用音]] : [[リ]]']
    ],
    '諺': [
        '音読み',
        ['[[呉音]] : [[ゲン]]'],
        ['[[漢音]] : ゲン'],
        ['[[慣用音]] : [[オン]]']
    ],
    '石': [
        '音読み',
        ['[[呉音]] : [[ジャク]]'],
        ['[[漢音]] : [[セキ]]'],
        ['[[慣用音]] : [[シャク]]、[[コク]]']
    ],
    '兄': [
        '音読み',
        ['[[呉音]] : [[キョウ]]（[[キャウ]]）'],
        ['[[漢音]] : [[ケイ]]']
    ],
    '皇': [
        '音読み',
        ['[[呉音]] : [[オウ]]([[ワゥ]])'],
        ['[[漢音]] : [[コウ]]([[クヮゥ]])']
    ],
    '谷': [
        '音読み',
        ['[[呉音]] : [[コク]]'],
        ['[[漢音]] : [[コク]]'],
    ],
    '間': [
        '音読み',
        ['[[呉音]] : [[ケン]]'],
        ['[[漢音]] : [[カン]]']
    ],
    '院': [
        '音読み',
        ['[[呉音]]：[[エン]]（[[ヱン]]）'],
        ['[[漢音]]：[[エン]]（[[ヱン]]）'],
        ['[[慣用音]]：[[イン]]、（[[ヰン]]）']
    ],
    '巻': [
        '音読み',
        ['[[呉音]] : [[ケン]]([[クヱン]])(表外)'],
        ['[[漢音]] : [[ケン]]([[クヱン]])(表外)'],
        ['[[慣用音]] : [[カン]]([[クヮン]])']
    ],
    '九': [
        '音読み',
        ['[[呉音]] : [[ク]]'],
        ['[[漢音]] : [[キュウ]]（[[キウ]]）'],
        ['[[唐音]] : キュウ（キウ）'],
        ['[[慣用音]] : [[クウ]]']
    ],
    '喰': [
        '音読み',
        ['[[呉音]] : [[ジキ]]、[[サン]]'],
        ['[[漢音]] : [[ショク]]、[[サン]]']
    ],
    '偽': [
        '音読み',
        ['[[呉音]]: [[ガ]]（[[グヮ]])(表外）、[[ギ]]（[[グヰ]]）'],
        ['[[漢音]]: [[ガ]]（[[グヮ]])(表外）、[[ギ]]（グヰ）'],
        ['[[慣用音]]: [[カ]]（[[クヮ]])(表外）']
    ],
    '中': [
        '音読み',
        ['[[呉音]] : [[チュウ]]、[[ジュウ]]（[[ヂュウ]]）'],
        ['[[漢音]] : [[チュウ]]、[[ジュウ]]（[[ヂュウ]]）']
    ],
    '別': [
        '音読み',
        ['[[呉音]] : [[ベチ]]（表外）'],
        ['[[漢音]] : [[ヘツ]]（表外）'],
        ['[[慣用音]] : [[ベツ]]']
    ],
    '欠': [
        '音読み',
        ['[[呉音]] : [[コン]]'],
        ['[[漢音]] : [[ケン]]'],
        ['[[慣用音]] : [[ケチ]]、[[ケツ]]']
    ]
}

def deal_special_cases(kanji, element):
    """
    Reconfigures the 'element' list for specific kanji characters based on predefined special cases.

    This function checks if the given kanji character has predefined special adjustments in the 'special_cases'
    dictionary. If a match is found, the 'element' list is modified according to the rules specific to that kanji.
    The adjustments generally modify the organization or number of elements in the 'element' list to tailor
    pronunciation data for specific needs, such as simplifying or emphasizing certain aspects based on discrepancies
    or complexities inherent to the kanji.

    Args:
        kanji (str): The kanji character under consideration for possible special adjustment.
        element (list): A list containing pronunciation data segments of the kanji, potentially to be modified.

    Returns:
        list: The modified 'element' list after applying special case adjustments, if any. If no special cases
              apply, the original 'element' list is returned unchanged.

    Notes:
        - The 'special_cases' dictionary directly encodes modifications for each kanji, specifying how the
          'element' list should be modified. Each key represents a kanji character and is associated
          with a value defining the new structure of 'element'.
        - The function acts primarily on the structure of the data within 'element', adding, removing,
          or rearranging the contained data as specified for certain kanji.
        - Examples of operations include truncating the list, reordering elements, or replacing the list with
          entirely new content specific to certain pronunciation categories.
    """

    if kanji in ["興", "曹", '漁', '算', "行", "蔵", "貪", "打"]:
        if kanji in ['曹', '興']:
            element = element[:3]
        if kanji in ['漁', '算']:
            element = element[:4]
        if kanji == '行':
            element = [element[0], element[1], element[3], element[5], element[6]]
        if kanji == '蔵':
            element = [element[0], element[1], element[3]]
        if kanji == '貪':
            element = [element[0], element[1], element[2], element[4]]
        if kanji == '打':
            element = [element[0], element[1], element[3], element[4]]
        return element
  
    # If the kanji is in the special_cases, update the 'element'
    if kanji in onyomi_special_cases:
        return onyomi_special_cases[kanji]
    
    # Keep the original if no special case applies
    return element  


def text_replacement(text):
    # remove [], replace full-width char to half-width, change others sign to space
    text = re.sub(r'[\[\]]', '', text[0])
    text = text.replace('（', '(').replace('）', ')').replace('：', ':')
    text = re.sub(r'、|・|　+|,|\'|\u3000', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    # remove additional info
    text = re.sub(r'<ref.*?</ref>', '', text)
    text = re.sub(r'<ref.*?/>', '', text)
    text = re.sub(r'Wiktionary:漢字索引\s*音訓\s*[^\|]*\|', '', text)
    text = re.sub(r':wikipedia:ja:[^\|]*\|', '', text)
    text = re.sub(r'{{要出典}}', '', text)

    # remove addtional info of value part which is the substring after ':' of text
    text = re.sub(r'\(例:[^\)]+\)', '', text)
    text = re.sub(r'\s+例．.*$', '', text)
    text = re.sub(r'\(\s*表外:.*\)', '(表外)', text)
    text = re.sub(r'\(表外[^\)]*\)', '(表外)', text)
    text = re.sub(r'{{音\|([^}]*)}}', r'\1', text)
    text = re.sub(r'[\u3041-\u3096]*\|([^\s*])', r'\1', text)

    # uniform value part of text
    text = re.sub(r'([^\s\(\)]*)\((\s*[^\s\(\)]*)\s+([^\s\(\)]*)\)', r"\1(\2)(\3)", text)
    text = re.sub(r'([^\s\(\)]*)\(\s*([^\s\(\)]*)\s+([^\s\(\)]*)\s+([^\s\(\)]*)\)', r"\1(\2)(\3)(\4)", text)

    # uniform string
    text = re.sub(r'\(([^:]+):[^\)]+\)', r'(\1)', text)

    # skip if there is no value
    if text.strip() == '無し':
        text = ""

    return text



def parse_values_structure(kanji, values):
    """
    Processes and structures '音読み' (On'yomi) readings from text extracted into key-value pairs.
    
    This function takes a kanji character and its associated readings, then parses and structures
    the readings into a standardized format. It handles complexities such as multiple readings,
    archaic pronunciations, and specific phonetic types by parsing the structured text. The extracted
    data is stored in dictionaries, which are collected into a list for further processing.

    Parameters:
        kanji (str): The kanji character for which the readings are being extracted and processed.
        values (str): The string containing '音読み' readings and related data, organized with structured markers.

    Process:
        1. The function first splits the input text by spaces to delineate individual readings.
        2. Each reading is parsed using regular expressions designed to extract multiple forms
           of readings and additional details like old pronunciations or specific phonetic types.
        3. Each extracted reading or detail is stored in a dictionary, considering special cases for
           non-standard readings or representation discrepancies.
        4. Pure katakana and hiragana values are directly converted or standardized respectively.
        5. The resultant dictionaries are added to a list, which could be used for further grouping
           or categorization.

    Returns:
        list: A list containing dictionaries. Each dictionary holds '音読み' related key-value pairs that
              have been standardized and cleansed for further processing.

    Notes:
        - This function is used within the broader context of parsing '音読み' readings from Wiktionary data.
        - Debugging and verification might print unexpected values or structural anomalies directly for human review.
    """
    values_dict = {}

    for raw_value in values.strip().split():
        # Initialize a dictionary to store the extracted information
        value = {}
        hougai_flag = False

        # Regex pattern to capture the main pronunciation, optional old pronunciations, and pronunciation type
        matched = re.match(r'^(?P<pron>[^\(]*)(\((?P<old_pron1>[^\)]*)\))?(\((?P<old_pron2>[^\)]*)\))?(\((?P<old_pron3>[^\)]*)\))?$', raw_value)

        for k, v in matched.groupdict().items():
            # Skip if the value is empty
            if not v:
                continue

            # Handle special cases such as "表外" (non-standard)
            if v in ['常用外', '表外']:
                hougai_flag = True
                continue

            # Flag to indicate if the value is pure katakana or pure hiragana
            pure_katakana_flag = True
            pure_hiragana_flag = True

            # Check if the value is pure katakana (using unicode range check)
            for ch in v:
                if ord(ch) >= 0x30a1 and ord(ch) <= 0x30ff or ord(ch) >= 0x1b132 and ord(ch) <= 0x1b167:
                    continue
                # Set the flag if a non-katakana character is found
                pure_katakana_flag = False
                break

            # If the value is pure katakana, assign the value directly
            if pure_katakana_flag:
                value[k] = v
                continue

            # Check if the value is pure hiragana (using unicode range check)
            for ch in v:
                if ord(ch) >= 0x3041 and ord(ch) <= 0x3096:
                    continue
                # Set the flag if a non-hiragana character is found
                pure_hiragana_flag = False
                break

            # Convert to katakana if the value is pure hiragana
            if pure_hiragana_flag:
                value[k] = ''.join([chr(ord(char) + 0x60) for char in v])
                continue

            # Print the values that don't follow the expected patterns for manual inspection
            #print(kanji, keys, k, v)
            #print(json.dumps(element, ensure_ascii=False, indent=4), '\n\n')

        # Add the processed value to the list
        if hougai_flag:
            if '表外' not in values_dict:
                values_dict['表外'] = []
            values_dict['表外'].append(value)
        else:
            if '表内' not in values_dict:
                values_dict['表内'] = []
            values_dict['表内'].append(value)

    return values_dict



def parse_onyomi_for_single_kanji(kanji, pron_arch):
    """
    Parses and organizes the '音読み' (On'yomi) readings of a given kanji from its pronunciation architecture.

    This function processes the hierarchical pronunciation data structure (`pron_arch`) extracted from
    wiktionary entries to specifically identify and categorize the '音読み' readings. It handles various
    formats and special cases in how these readings are presented in the data, cleaning and structuring
    the output into a dictionary format.

    Args:
        kanji (str): The kanji character for which '音読み' readings are being extracted.
        pron_arch (list): A hierarchical list representing pronunciation data, structured based on
                          levels and categories as parsed from the source wikitext. An example structure
                          for the kanji '戮' is shown in the docstring example below.

    Returns:
        dict: A dictionary where keys represent different '音読み' categories (e.g., '漢音', '呉音', '慣用音')
              and the values are lists of dictionaries. Each inner dictionary contains the reading ('pron') 
              and potentially additional information about the reading like 'type' or 'old_pron'. 
              If no '音読み' data is found, an empty dictionary is returned.

    Example:
        >>> pron_arch = [
        ...     [
        ...         ' 音読み',
        ...         [
        ...             ' [[呉音]] : [[ロク]]'
        ...         ],
        ...         [
        ...             ' [[漢音]] : [[リク]]'
        ...         ]
        ...     ],
        ...     [
        ...         ' 訓読み',
        ...         [
        ...             ': [[ころす|ころ-す]]、[[けずる|けず-る]]、[[あわす|あわ-す]]'
        ...         ]
        ...     ]
        ... ]
        >>> parsing_onyomi('戮', pron_arch)
        {'呉音': [{'pron': 'ロク'}], '漢音': [{'pron': 'リク'}]}

    Notes:
        - The function includes extensive hardcoded handling of specific formats and edge cases observed
          in the wikitext for different kanji, particularly involving the structure and variations in
          how '音読み' readings are listed.
        - Regular expressions are extensively used for text cleaning and extraction of relevant information
          from the raw pronunciation data.
        - The function makes assumptions about the structure and presence of certain keywords in the
          `pron_arch` input based on the typical format of Japanese pronunciation sections in Wiktionary.
    """

    # If there is no pronunciation architecture data, return an empty dictionary
    if not len(pron_arch):
        return {}
    
    # Define a mapping for key names to standardize variations
    key_name_map = {
        "宋音": "宋唐音",
        "唐音": "宋唐音",
        "唐宋音": "宋唐音",
        "唐音唐宋音": "宋唐音",
        "新漢音": "漢音",
        "特殊な慣用音": "慣用音",
        "古音": "慣用音",
    }

    
    sub_kanji_elements = []
    for element in pron_arch:
        """
        Each element is a sub kanji character, which means the single kanji used as several kanji characters in different context.
        an exmple of element, which is a list of list:
        [
            ' 音読み',
            [
                ' [[呉音]] : [[ロク]]'
            ],
            [
                ' [[漢音]] : [[リク]]'
            ]
        ]
        """
        if not element:
            continue

        if '音読み' not in element[0]:
            continue
        
        sub_kanji_elements.append(element)
        

    sub_kanji_onyomi = {}

    count_sub_kanji = len(sub_kanji_elements)
    for index, element in enumerate(sub_kanji_elements, start=1):
        # give new value for specific kanji characters which has abnormal element.
        element = deal_special_cases(kanji, element)

        onyomi = {}
        for text in element[1:]:
            if type(text) == str:
                continue

            text = text_replacement(text)
            if not text:
                continue

            keys, values = text.split(':')
            key_list = [key_name_map[key] if key in key_name_map else key for key in keys.strip().split()]
            values_dict = parse_values_structure(kanji, values)
            #print(kanji, key_list, values_dict)
            
            for yomi_type_key in key_list:
                onyomi[yomi_type_key] = values_dict

        if count_sub_kanji > 1:
            sub_kanji_key = f"{kanji}{index}"
        else:
            sub_kanji_key = kanji
        sub_kanji_onyomi[sub_kanji_key] = onyomi
    
    """
    DEBUG:
    if any([key.startswith('画') or key.startswith('畫') for key in sub_kanji_onyomi.keys()]):
        print(sub_kanji_onyomi)
    """
        
    return sub_kanji_onyomi
        


def parse_onyomi(pron_arch_dict):
    """
    Parse the onyomi information from the pronunciation architecture dictionary.

    This function takes a dictionary of pronunciation architectures and parses the onyomi information
    for each kanji. It returns a dictionary of onyomi information and a dictionary of all the keys found.

    Args:
        pron_arch_dict (dict): A dictionary where keys are kanji characters and values are lists of strings
    """
    onyomi_dict, all_onyomi_keys = {}, {}

    for kanji, pron_arch in pron_arch_dict.items():
        single = parse_onyomi_for_single_kanji(kanji, pron_arch)
        onyomi_dict.update(single)
        
        for value in single.values():
            for key in value:
                all_onyomi_keys[key] = all_onyomi_keys.get(key, 0) + 1
 
    return onyomi_dict, all_onyomi_keys
