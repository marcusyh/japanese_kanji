from kanji.jouyou import load_jouyou
from kanji.jinmei import load_jinmei
from kanji.hyougai import load_hyougai
from kanji.itai import load_itai


def load_local_kanji():
    # kanji_dict used to save the respected result. 
    # The kanji which has the smallest unicode value of the itai kanji group will be treated as the key
    # All the kanji of the itai kanji group will be put in the value list
    """
    {
        '亜': {
            "kanji": [1亜, 1亞],
            'kana': {
                'ア': '亜流 亜麻 亜熱帯'
            }
        },
        '哀': {
            'kanji': [1哀],
            'kana': {
                'アイ': '哀愁 哀願 悲哀',
                'あわれ': '哀れ 哀れな話 哀れがる',
                'あわれむ': '哀れむ 哀れみ'
            },
        }
        ...
    }
    """
    kanji_dict = {}

    # An assistant dictionary
    # Any kanji appearred as the key, the key in kanji_dict as the value of them.
    temp_dict= {}

    jouyou = load_jouyou()
    hyougai = load_hyougai()
    jinmei = load_jinmei()
    itai = load_itai()

    # merge these 4 kinds of source data
    for index, source in enumerate([jouyou, hyougai, jinmei, itai], start=1):
        for ji, kana in source.items():
            appendix = str(index)

            if ji.strip().strip('/') == '':
                continue

            items = sorted(ji.split('/'))
            matched = [item for item in items if item in temp_dict]
            mismatched = list(set(items) - set(matched))
            
            # when matched list is empty, append all element in items list to kanji_dict with key items[0]
            if not matched:
                kanji_dict[items[0]] = {
                        'kanji': [appendix + item for item in items],
                        'kana': kana}
                temp_dict.update({item: items[0] for item in items})
                continue
            
            # following code block dealing with the condition when matched list is not emppty
            repesentative = temp_dict[matched[0]]

            # when items[0] is equal or bigger than the original key in kanji_dict, 
            # we still let the orignal key as the key
            if items[0] == repesentative or sorted([items[0], repesentative])[0] == repesentative:
                kanji_dict[repesentative]['kanji'] += [appendix + item for item in mismatched]
                kanji_dict[repesentative]['kana'].update(kana)
                temp_dict.update({item: repesentative for item in mismatched})
                continue
            
            # when items[0] is smaller than the orignal key, 
            # we replace the original key to items[0] 
            items2 = sorted(mismatched + [item[1] for item in kanji_dict[repesentative]['kanji']])
            kanji_dict[repesentative]['kanji'] += [appendix + item for item in mismatched]
            kanji_dict[repesentative]['kana'].update(kana)
            kanji_dict[items2[0]] = kanji_dict[repesentative]
            del kanji_dict[repesentative]
            temp_dict.update({item: items[0] for item in items2})

    kanji_list = []
    for key in sorted(kanji_dict):
        item = kanji_dict[key]
        kanji_list += [kanji[-1] for kanji in item['kanji']]
    return kanji_dict, kanji_list



def load_local_kanji_without_tag():
    """
    Returns:
        {
        '亜': {亜, 亞},
        '哀': {哀}
        ...
    }
    """
    # Initialize a dictionary to store kanji groupings
    kanji_dict = {}

    # Load various sets of kanji characters from different categories
    jouyou = load_jouyou()
    hyougai = load_hyougai()
    jinmei = load_jinmei()
    itai = load_itai()
    
    # Combine keys from all dictionaries and iterate through them
    for kanji_str in list(jouyou.keys()) + list(jinmei.keys()) + list(hyougai.keys()) + list(itai.keys()):
        # Split each key on '/' to handle kanji groups, and then sort them
        kanji_group = sorted(kanji_str.split('/'))
        
        # Skip processing if no kanji exist
        if len(kanji_group) < 1:
            continue
        
        # Check if any kanji already exists in the kanji_dict to avoid duplicate entries
        # merge kanji_group to already exists entry in kanji_dict
        for kanji in kanji_group:
            if kanji in kanji_dict:
                break

        # Set the first kanji (smallest after sorting) as the key in kanji_dict
        # Combines its current value with the new kanji_group set, ensuring no duplications
        kanji_dict[kanji_group[0]] = set.union(kanji_dict.get(kanji, set()), set(kanji_group))
        
        # Clean out duplicate entries and ensure only representative kanji remains as the key
        if kanji_group.index(kanji) != 0 and kanji in kanji_dict:
            del kanji_dict[kanji]

    # Return the dictionary of grouped kanji characters
    return kanji_dict


if __name__ == '__main__':
    from save_file import convert_to_writable, save_to_docx, save_to_csv
    kanji_result, kanji_list = load_local_kanji()
    print(len(kanji_list), len(kanji_result))
    print(kanji_list)
    wrtb = convert_to_writable(kanji_result)
    save_to_csv(wrtb, 'test.csv', '/tmp/')
    save_to_docx(wrtb, 'test.docx', '漢字の音読み', '/tmp/')
