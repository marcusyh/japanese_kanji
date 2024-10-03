
import copy
from wikt_parser.utils import parsing_pron_arch_build_tree
from wikt_parser.ja_filter import select_ja_pronucation
from wikt_cache.patch import load_patch


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



def parse_pron_arch(pron):
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


    # Check if pronunciation data is minimal, returning empty dictionary if insufficient data
    if len(pron) <= 1:
        return {}
    
    arch_tree = create_hierarchical_tree(pron)
    arch_tree = merge_kunyomi(arch_tree)
    arch_tree = merge_onyomi(arch_tree)
    arch_tree = fix_mistaken_group(arch_tree)

    # Return the final architecture tree derived from pronunciation data
    return arch_tree



def create_ja_pron_arch(wiki_dict):
    """
        Create pronunciation architecture for each kanji
    """
    pron_arch_all = {}
    for kanji, details in wiki_dict.items():
        pron_text = select_ja_pronucation(details)
        pron_arch = parse_pron_arch(pron_text)
        pron_arch_all[kanji] = pron_arch

    patch_pron_arch = load_patch()
    for kanji, pron_arch in patch_pron_arch.items():
        pron_arch_all[kanji] = pron_arch
        
    return pron_arch_all
