from wiktionary.cache import WikiCache
from wiktionary.utils import split_groups
from wiktionary.ja.pron_arch import parse_pron_arch
from wiktionary.ja.onyomi import process_onyomi


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

    


# create a function to generate a markdown table by the oyomi result which is generated by the function parsing_onyomi
def generate_markdown_table(kanjis, onyomi):
    for kanji in kanjis:
        if kanji not in onyomi:
            continue
        print(kanji)
        print('| 音読み | 漢音 | 唐音 | 慣用音 |')
        print('| --- | --- | --- | --- |')
        for key, value in onyomi[kanji].items():
            print('|', key, '|', value['漢音'], '|', value['唐音'], '|', value['慣用音'], '|')
        print()


def parsing_ja(wiki_cache):
    wiki_dict = {}
    for kanji, details_texts in wiki_cache.wiki_dict.items():
        details_groups = split_groups(kanji, details_texts[0])
        wiki_dict[kanji] = details_groups

    pron_arch_all = {}
    for kanji, details in wiki_dict.items():
        pron_text = select_ja_pronucation(details)
        pron_arch = parse_pron_arch(pron_text)
        pron_arch_all[kanji] = pron_arch
        
    return pron_arch_all