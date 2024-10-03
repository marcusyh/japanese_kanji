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