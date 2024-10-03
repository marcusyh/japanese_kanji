import re

def split_groups_for_each_kanji(k, wikitext):
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



def split_groups(wiki_dict):
    kanji_dict = {}
    for kanji, details_texts in wiki_dict.items():
        details_groups = split_groups_for_each_kanji(kanji, details_texts[0])
        kanji_dict[kanji] = details_groups

    return kanji_dict