import re


def fileter_characters(input):
    output = []
    for char in input:
        value = ord(char)
        # ascii a-z
        # ascii A-Z
        # full width hiragana: 0x3041 -- 0x3096
        # full width katakana: 0x30A0 -- 0x30FF
        # Katakana Phonetic Extensions(片仮名拡張): 0x31F0--0x31FF
        # all CJK kanji: 0x3400 -- 0x4DB5, 0x4E00 -- 0x9FCB, 0xF900 -- 0xFA6A
        # character: 0x3005
        # Japanese point: 0xff65
        # Kana Supplement(仮名補助): 0x1b000--0x1b0ff
        # Kana Extended-A(仮名拡張A): 0x1B100--0x1B12F
        # Kana Extended-B(仮名拡張B): 0x1AFF0--0x1AFFF
        # Small Kana Extension(小書き仮名拡張): 0x1b132, 0x1b150--0x1b152, 0x1b155, 0x1b164--0x1b167

        if value >= 0x41 and value <= 0x5a \
        or value >= 0x61 and value <= 0x7a \
        or value >= 0x3041 and value <= 0x3096 \
        or value >= 0x30a1 and value <= 0x30ff \
        or value >= 0x3400 and value <= 0x4db5 \
        or value >= 0x4e00 and value <= 0x9fcb \
        or value >= 0xf900 and value <= 0xfa6a \
        or value >= 0x1b132 and value <= 0x1b167 \
        or value in [0x3005, 0xff65]:
            output.append(char)

    return ''.join(output) 


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
        The output structure:
            {
                'Header1': [1, 'Content line', ...],
                'Header2': [2, 'Content line', ...],
                ...
            }

    Example:
        Input:
        '''
            =={{ja}}==
            [[Category:{{ja}}|りく]]

            ==={{pron|jpn}}===
            * 音読み
            ** [[呉音]] : [[ロク]]
            ** [[漢音]] : [[リク]]
            * 訓読み
            *: [[ころす|ころ-す]]、[[けずる|けず-る]]、[[あわす|あわ-す]]

            ==={{prov}}===
            * [[刑戮]]
            * [[殺戮]]
            * [[誅戮]]

            ----
        '''

        Output:
        {
            '{{ja}}': [
                2, 
                '[[Category:{{ja}}|りく]]'
            ],
            '{{pron|jpn}}': [
                3,
                '* 音読み',
                '** [[呉音]] : [[ロク]]',
                '** [[漢音]] : [[リク]]',
                '* 訓読み',
                '*: [[ころす|ころ-す]]、[[けずる|けず-る]]、[[あわす|あわ-す]]'
            ],
            '{{prov}}': [
                3,
                '* [[刑戮]]',
                '* [[殺戮]]',
                '* [[誅戮]]',
                '----'
            ]
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



def parsing_pron_arch_build_tree(levels, texts):
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
            result.append([previous_text] + parsing_pron_arch_build_tree(sub_levels, sub_texts))
            sub_texts = []
            sub_levels = []
        
        # Update previous_text to be the new block's header key
        previous_text = text
    
    # After loop, process last accumulated sublist to ensure all texts are linked to the right headers
    result.append([previous_text] + parsing_pron_arch_build_tree(sub_levels, sub_texts))

    # Return the constructed tree-like dictionary
    return result