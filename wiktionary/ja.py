import re
from cache import WikiCache

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

        if k in ['戻', '野']:
            print(header, sub_group)
    if k in ['戻', '野']:
        print(result,'\n\n')

    # After the loop, save the last processed header and its contents to the result
    result[header] = sub_group

    return result


#===== 語義1 =====
#==== 用法1-4 ====


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

    # Initialize an empty list to store Japanese pronunciation details.
    ja_pron = []

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
            ja_pron.append(value)
            break
    if ja_pron:
        return ja_pron

    # Second pass check: look for key directly containing '読み' indicating readings.
    # Return found pronunciation if any.
    for key, value in tmp_dict.items():
        if '読み' in key and '読み' in value:
            ja_pron.append(value)
            break
    if ja_pron:
        return ja_pron
    
    # Third pass check: seek alternative representations potentially using '発音' indicating phonetic descriptions.
    # Return the collected pronunciations if any were fetched.
    for key, value in tmp_dict.items():
        if '発音' in key and '読み' in value:
            ja_pron.append(value)
            break
    if ja_pron:
        return ja_pron

"""

        '===={{pron}}====',
            '* 音読み   :',
                '** [[呉音]] : [[ニュウ]]（ニフ:[[入声]]であり無声子音の前では、「ニッ」となる）',
                '** [[漢音]] : [[ジュウ]]（ジフ）',
                '** [[慣用音]] : [[ジュ]]',
            '* 訓読み   : [[いる|い-る]]、[[いれる|い−れる]、][[はいる|はい-る]]､[[しお]]',

"""

if __name__ == '__main__':
    wc = WikiCache()
    wiki_dict = {}
    for k, v in wc.wiki_dict.items():
        v = split_groups(k, v[0])
        wiki_dict[k] = v


    a = {}
    for k, v in wiki_dict.items():
        found = select_ja_pronucation(v)
        if not found:
            print(k, v, '\n\n')
