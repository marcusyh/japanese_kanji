import re
import copy
from cache import WikiCache
from utils import fileter_characters

def split_groups(k, wikitext):
    """
    Parses the provided wikitext for a given kanji entry and organizes it into a structured dictionary.
    
    This function iterates through lines of wikitext and classifies them into sections and subsections
    based on their header levels. Non-header lines are gathered into lists that represent the content
    under their respective headers.
    
    Parameters:
        wikitext (str): The string of wikitext that includes textual data possibly containing headers and 
                        structured information.
    
    Returns:
        dict: A dictionary where each key is a header title and each value is a list that begins with a 
              tuple containing the header title and its level, followed by the content lines under that 
              header.
              
    Example of structure:
        {
            'Header1': [1, 'Content line', ...],
            'Header2': [2, 'Content line', ...],
            ...
        }
    """
    # Initialize an empty dictionary to hold structured data parsed from wikitext
    result = {}

    # Initialize sub group value
    sub_group = [] # List to keep track of subsections in the wikitext
    header = None  # To hold the current header name

    # Iterating over each line in the wikitext
    for line in wikitext.split('\n'):

        # Skipping empty lines
        if line.strip() == "":
            continue
        
        # Remove leading and trailing whitespace, as well as HTML comments from the line
        line = line.strip()
        line = re.sub(r'\s*<!--[^->]*-->\s*', '', line)
        
        # If the line is a header (i.e., enclosed in equal signs), it's header of wikitext
        if line.startswith('=') and line.endswith('='):

            # Check if there's an ongoing header; if so, store accumulated lines in result
            if header:
                if header not in result:
                    result[header] = []
                result[header] += sub_group

            # when meet a new header
            header = line.strip('=').strip() # Reset header to the new header and strip the surrounding equal signs
            level = line.count('=') // 2     # Determine the header level based on the number of equal signs
            sub_group = [level]
    
        else:
            # Add non-header lines to the sub_group
            sub_group.append(line.strip())

    # After the loop, save the last processed header and its contents to the result
    result[header] = sub_group

    return result



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


def _parsing_pron_arch_build_tree(levels, texts):
    """
    Constructs a hierarchical tree representation from provided text and their associated levels.

    This function recursively generates a nested list where the first element of each list is a text header 
    corresponding to a 'level' of 0, and the following items in the list representing sub-levels and their 
    corresponding texts. The recursion continues down through levels creating a tree-like structure.

    Args:
        levels (list of int): List of integers where each integer represents the hierarchical level of the 
                              associated text in 'texts'. The base level (1) starts a new branch in the 
                              resulting tree.
        texts (list of str): List of strings corresponding to different elements extracted from wikitext, 
                             typically as headers and their subsequent data.

    Returns:
        dict: A nested list representing the hierarchical structure of headers and data. Each 'level' 
              of 1 in 'levels' starts a new list, with the value being the recursive call to handle 
              all subsequent sub-levels and texts.
              
    Example:
        Input: 
            levels = [1, 2, 3, 2, 1, 2]
            texts = ["text1", "text1.1", "text1.1.1", "text1.2", "text2", "text2.1"]
        Output:
            [
                "text1", ["text1.1", "text1.1.1"], "text1.2",
            ],
            [
                "text2", "text2.1"
            ]
    """
    # Check if there are no levels provided (base case for recursion), return an empty dictionary
    if not levels:
        return []
    
    # Create an empty dictionary where the results of parsing will be stored
    result = []
    
    # Decrease each level by one to facilitate sub-level parsing relative to the current level
    new_levels = levels
    while min(new_levels):
        new_levels = [x-1 for x in new_levels]

    # Initialize lists to store sub-levels and sub-texts that will compose subtrees
    sub_levels = []
    sub_texts = []
    
    # Variable to store the current header text to be used as a key for sub-trees
    previous_text = None
    
    # Iterate through each level and its corresponding text
    for index, level in enumerate(new_levels):
        text = texts[index]
        
        # If the level is non-zero, it indicates it is a sub-level to the current block
        if level:
            sub_levels.append(level)
            sub_texts.append(text)
            continue
        
        # Encountering a zero level: wrap up/sub-tree the previous block and start a new one
        if previous_text:
            result.append([previous_text] + _parsing_pron_arch_build_tree(sub_levels, sub_texts))
            sub_texts = []
            sub_levels = []
        
        # Update previous_text to be the new block's header key
        previous_text = text
    
    # After loop, process last accumulated sublist to ensure all texts are linked to the right headers
    result.append([previous_text] + _parsing_pron_arch_build_tree(sub_levels, sub_texts))

    # Return the constructed tree-like dictionary
    return result
    

def parsing_pron_arch(kanji, pron):
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
        arch_tree = _parsing_pron_arch_build_tree(levels, texts)

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
                print(kanji, len(arch_tree), arch_tree)
        
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



if __name__ == '__main__':
    wc = WikiCache()
    wiki_dict = {}
    for k, v in wc.wiki_dict.items():
        v = split_groups(k, v[0])
        wiki_dict[k] = v


    a = {}
    for k, v in wiki_dict.items():
        found = select_ja_pronucation(v)
        parsing_pron_arch(k, found)
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
