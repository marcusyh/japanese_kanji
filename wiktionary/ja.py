import re
import copy
from cache import WikiCache
from utils import fileter_characters, split_groups, parsing_pron_arch_build_tree


def select_ja_pronucation(wikitionary):
    """
    Extracts Japanese pronunciation information from a structured wikitionary entry.

    This function searches for Japanese pronunciation data within a structured dictionary
    derived from a parsed wikitext, focusing on specific keys and contents that typically 
    contain phonetic information. The search is conducted in multiple passes, targeting
    different likely keys and formats in which pronunciation details are presented.

    Parameters:
        wikitionary (dict): A dictionary where each key typically corresponds to a header in the wikitext,
                            with values being lists containing the header level and content under that header.

    Returns:
        list: A list of strings containing the found pronunciation content. If no specific pronunciation
              data is identified, an empty list is returned.

    The function operates in multiple sequential 'passes':
        1. Searches for keys containing 'pron' and checks if their corresponding values contain '読み'.
        2. If the first pass fails, it searches for any key directly containing '読み'.
        3. If the second pass also fails, it looks for keys containing '発音' with values that include '読み'.

    Each of these passes returns immediately if it finds relevant data, skipping subsequent searches.

    Output Example:
        [
            3,
            '* 音読み',
            '** [[呉音]] : [[ロク]]',
            '** [[漢音]] : [[リク]]',
            '* 訓読み',
            '*: [[ころす|ころ-す]]、[[けずる|けず-る]]、[[あわす|あわ-す]]'
        ]
    """

    # Initialize an empty dictionary to build a simplified structure from the passed wikitionary.
    tmp_dict = {}
    # Iterate through the dictionary, concatenating values that are not header levels (integers) into strings.
    for key, value in wikitionary.items():
        if not key:
            continue
        # Concatenate list of strings into a single string, excluding integers (header levels).
        tmp_dict[key] = ''.join([x for x in value if type(x) != int])
    
    # First pass check: look for sections that likely contain pronunciation data using "pron" in key.
    # If a pronunciation is found, return it.
    for key, value in tmp_dict.items():
        if 'pron' in key and '読み' in value:
            return wikitionary[key]

    # Second pass check: look for key directly containing '読み' indicating readings.
    # Return found pronunciation if any.
    for key, value in tmp_dict.items():
        if '読み' in key and '読み' in value:
            return wikitionary[key]
    
    # Third pass check: seek alternative representations potentially using '発音' indicating phonetic descriptions.
    # Return the collected pronunciations if any were fetched.
    for key, value in tmp_dict.items():
        if '発音' in key and '読み' in value:
            return wikitionary[key]

    return []

    

def parsing_pron_arch(pron):
    """
    Parses hierarchical pronunciation architecture from a given list of pronunciation data.

    This function builds a structured hierarchical tree from Japanese kanji pronunciation text data which
    is represented by a list where the first item is the header level followed by the respective contents.
    It specifically processes and organizes data into meaningful clusters such as '音読み' (on'yomi) and '訓読み' (kun'yomi),
    handling various special cases and merging related sections.

    Args:
        kanji (str): The kanji character key for which pronunciation data is being parsed.
        pron (list): A list containing pronunciation data. The first element indicates the hierarchical
                     level followed by strings containing the actual pronunciation details.
                     Here is an example of the pron input:
                        '* 音読み   :',
                            '** [[呉音]] : [[ニュウ]]（ニフ:[[入声]]であり無声子音の前では、「ニッ」となる）',
                            '** [[漢音]] : [[ジュウ]]（ジフ）',
                            '** [[慣用音]] : [[ジュ]]',
                        '* 訓読み   : [[いる|い-る]]、[[いれる|い−れる]、][[はいる|はい-る]]､[[しお]]',

    Returns:
        list: A structured list where nested sub-lists represent hierarchical pronunciation sections and details.
              The formatting reflects pronunciation categorizations like '音読み' and '訓読み'.
              Here is the ouput list of the abouve pron input:
              [
                [
                    '音読み   :',
                    '[[呉音]] : [[ニュウ]]（ニフ:[[入声]]であり無声子音の前では、「ニッ」となる）',
                    '[[漢音]] : [[ジュウ]]（ジフ）',
                    '[[慣用音]] : [[ジュ]]''
                ],
                [
                    '訓読み   : [[いる|い-る]]、[[いれる|い−れる]、][[はいる|はい-る]]､[[しお]]'
                ]
              ]

    Additional Notes:
        - The function heavily relies on recognizing key terms (e.g., '音読み', '訓読み') and hierarchy markers
          (asterisks) in the input list to organize the pronunciation data.
        - Special handling includes merging segments under '音読み' if they're solitary, rechecking sentence
          fragments erroneously included, and reassigning '訓読み' sections.
        - The function outputs a deeply nested list where each inner list corresponds to a hierarchy level
          in the context of Japanese pronunciation classification.
    """

    def create_hierarchical_tree(pron):
        """
        Constructs a hierarchical tree based on the pronunciation annotation format found in the input list.

        This function is designed to interpret the structured pronunciation data representing different levels
        of pronunciation details in the 'pron' list. It processes this list to create a hierarchical tree structure
        where each node represents a certain level of detail or categorization in the pronunciation data.

        The input list is expected to have pronunciation entries starting with asterisks '*', which indicate the
        hierarchical level. Each higher number of asterisks denotes a deeper level in the hierarchy. This function
        strips the asterisks to determine the level and extracts the meaningful text to construct a hierarchy tree.

        Args:
            pron (list): A list containing pronunciation data beginning with a header level followed by strings.
                        Each string represents a pronunciation detail at a certain level indicated by the asterisks.
                        Example input:
                            [
                                3,
                                '* Level 1 Pronunciation',
                                '** Level 2 Detail',
                                '*** Level 3 More Specific Detail'
                            ]

        Returns:
            list: A hierarchical structure list, where each sub-list represents a node in the tree that corresponds to
                a level of pronunciation detail. The structure and depth of the list reflect the categorization and
                specificity of pronunciation as indicated by the original asterisks.
                Example output:
                    [
                        ['Level 1 Pronunciation', 
                            ['Level 2 Detail',
                                ['Level 3 More Specific Detail']
                            ]
                        ]
                    ]

        Notes:
            - The function expects the first element of the input 'pron' list to be a numerical header level,
            which is omitted from processing.
            - Only strings that start with '*' are considered for processing, indicating their relevance 
            in the pronunciation hierarchy.
            - The intermediate processing involves stripping asterisks and counting them to determine the
            hierarchical levels, which are essential for constructing the return structure.
        """
        texts = []  # This will store the stripped text content of the entries
        levels = []  # This will store the level of each entry for hierarchy construction
        
        # Prepare for the building hierarchical tree structure 
        for index, item in enumerate(pron[1:]):
            # Skip items that are not strings
            if type(item) != str:
                    continue
            # Skip strings that don't start with asterisks which designate levels
            if not item.startswith('*'):
                continue
            # Strip the leading asterisks and determine the level by the number of removed asterisks
            striped = item.lstrip('*')
            levels.append(len(item) - len(striped))
            texts.append(striped)

        # Build hierarchical tree structure from level and text data
        arch_tree = parsing_pron_arch_build_tree(levels, texts)

        return arch_tree


    def merge_kunyomi(arch_tree):
        # merge '訓読み' elements to a whole list as an element of the top hierarchical tree structure level
        kunyomi_merge = False  # Flag to check if '訓読み' merging is needed
        # Check if any segment should merge together to form '訓読み' element of the top hierarchical tree structure level
        for index, item in enumerate(arch_tree):
            if index+1 < len(arch_tree) and '訓読み' in item[0]:
                kunyomi_merge = True
                break
        # Perform merging of current '訓読み' with subsequent segments
        if kunyomi_merge:
            tmp = copy.deepcopy(arch_tree[:index+1])
            tmp[index] += arch_tree[index+1:]
            arch_tree = tmp
    
        return arch_tree
    

    def merge_onyomi(arch_tree):
        # Special case handling if '音読み' exists and is solitary without associated details
        if len(arch_tree) >= 2 and '音読み' in arch_tree[0][0] and len(arch_tree[0]) == 1:
            # Check the second segment for keywords indicating omission or absence and merge if found
            for word in ["無し", "なし"]:
                if word in arch_tree[1][0]:
                    arch_tree[0] += arch_tree[1]
                    arch_tree.remove(arch_tree[1])
                    break

        # Reorganize tree structure for '音読み' and '訓読み' sections
        if len(arch_tree) > 2:
            start_index, end_index = 1, 1
            for index, item in enumerate(arch_tree[1:], start=1):
                if '音読み' in item[0]:
                    start_index += 1
                    continue
                if '訓読み' in item[0]:
                    end_index = index
                    break
            if start_index < end_index:
                new_arch_tree = arch_tree[:start_index]
                new_arch_tree[start_index-1] += arch_tree[start_index:end_index]
                new_arch_tree += arch_tree[end_index:]
                arch_tree = new_arch_tree

        return arch_tree
    
    
    def fix_mistaken_group(arch_tree):
        # Additional checks focusing only if '音読み' exists alone
        # check the '訓読み'  elements which was mistaken grouped to '音読み',
        # move them to the seprated  '訓読み' group if found
        if len(arch_tree) == 1 and '音読み' in arch_tree[0][0]:
            kunyomi_start_index = None
            # Scan through segments to flag where '訓読み' or related keywords occur
            for index, item in enumerate(arch_tree[0]):
                if type(item) == str:
                    found_flag = False
                    for keyword in ['常用漢字表内', '常用漢字表外', '訓読み']:
                        if keyword in item:
                            found_flag = True
                            break
                if type(item) == list:
                    found_flag = False
                    for str_item in item:
                        for keyword in ['常用漢字表内', '常用漢字表外', '訓読み']:
                            if keyword in str_item:
                                found_flag = True
                                break
                        if found_flag:
                            break
                if found_flag:
                    kunyomi_start_index = index
                    break
            if kunyomi_start_index:
                new_arch_tree = []
                new_arch_tree.append(arch_tree[0][:kunyomi_start_index])
                kunyomi = arch_tree[0][kunyomi_start_index:]
                if '訓読み' not in kunyomi[0]:
                    kunyomi.insert(0, '訓読み')
                new_arch_tree.append(kunyomi)
                arch_tree = new_arch_tree
        
        return arch_tree


    # Check if pronunciation data is minimal, returning empty dictionary if insufficient data
    if len(pron) <= 1:
        return {}
    
    arch_tree = create_hierarchical_tree(pron)
    arch_tree = merge_kunyomi(arch_tree)
    arch_tree = merge_onyomi(arch_tree)
    arch_tree = fix_mistaken_group(arch_tree)

    # Return the final architecture tree derived from pronunciation data
    return arch_tree


def parsing_onyomi(kanji, pron_arch):
    """
    pron_arch example of kanji '戮':
    [
        [
            ' 音読み',
            [
                ' [[呉音]] : [[ロク]]'
            ],
            [
                ' [[漢音]] : [[リク]]'
            ]
        ],
        [
            ' 訓読み',
            [
                ': [[ころす|ころ-す]]、[[けずる|けず-る]]、[[あわす|あわ-す]]'
            ]
        ]
    ]
    """
    if not len(pron_arch):
        return {}
    
    flag = False
    onyomi = {}
    for element in pron_arch:
        """
        an exmple of element[1:]
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

        if kanji in ['漁', '算']:
            element = element[:4]
        if kanji == '行':
            element = [element[0], element[1], element[3], element[5], element[6]]
        if kanji == '蔵':
            element = [element[0], element[1], element[3]]
        if kanji == '法':
            element = [
                ' 音読み',
                ['[[呉音]]: [[ホウ]]、[[ホフ]]、[[ホッ]]'],
                ['[[漢音]]: [[ホウ]]、[[ハフ]]、[[ハッ]]']
            ]
        if kanji == '合':
            element = [
                ' 音読み',
                [' [[呉音]] : [[ゴウ]]、[[ガフ]]、[[ガッ]]'],
                [' [[漢音]] : [[コウ]]、[[カフ]]、[[カッ]]']
            ]
        if kanji == '月':
            element = [
                '音読み',
                [' [[呉音]] : [[ガチ]]（グヮチ）、[[ガツ]]（グヮツ）'],
                [' [[漢音]] : [[ゲツ]]（グヱツ）'],
                [' [[慣用音]] : [[ガツ]]（グヮツ）']
            ]
        for text in element[1:]:
            if type(text) == str:
                continue

            # some kanji has specifal format
            if kanji in ['十', '貼', '禅', '作']:
                text = text[:1]
            if kanji == '芸':
                if text[0] == ':「藝」の[[新字体]]':
                    continue
                else:
                    text = text[1]
            if kanji == '央':
                if text[0] == '一':
                    text = text[1]
                else:
                    continue
            if kanji == '灯':
                continue

            # remove [], addtional info, uniform charcters
            value = re.sub(r'[\[\]]', '', text[0])
            value = re.sub(r'<ref.*?</ref>', '', value)
            value = re.sub(r'<ref.*?/>', '', value)
            value = value.replace('（', '(').replace('）', ')').replace('：', ':')
            value = re.sub(r'\(表外[^\)]*\)', '(表外)', value)
            value = re.sub(r'Wiktionary:漢字索引\s*音訓\s*[^\|]*\|', '', value)
            value = re.sub(r':wikipedia:ja:[^\|]*\|', '', value)
            value = re.sub(r'\(例:[^\)]+\)', '', value)
            #value = re.sub(r'(\([^\)]*\))\([^\)]*\)', '(\1)', value)
            value = re.sub(r'\(([^:]+):[^\)]+\)', r'(\1)', value)
            if value.strip() == '無し':
                continue
            x = value.split(':')
            print(kanji, x)
            if len(x) != 2:
                print(kanji, value, [i.strip() for i in x])

def parsing_ja():
    wc = WikiCache()
    wiki_dict = {}
    for kanji, details_texts in wc.wiki_dict.items():
        details_groups = split_groups(kanji, details_texts[0])
        wiki_dict[kanji] = details_groups

    pronounce = {}
    for kanji, details in wiki_dict.items():
        pron_text = select_ja_pronucation(details)
        pron_arch = parsing_pron_arch(pron_text)
        parsing_onyomi(kanji, pron_arch)
        
    """
        if not found:
            continue
        x = len(found)
        if x not in a:
            a[x] = [0, found]
        a[x][0] += 1

    for k in sorted(a):
        print(k, a[k])
    print(a)
    """

if __name__ == '__main__':
    parsing_ja()