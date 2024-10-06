
from wikt_parser import parse_ja_yomi
from output.formater import generate_yomi_rows
from output.yomi_printer import output_yomi_info

def generate_headers(duplicate_by_all, show_old_pron, show_hyogai):
    headers = ["", "音序"] if duplicate_by_all else []
    for reading_type in ['呉音', '漢音', '宋唐音', '慣用音']:
        headers.append(reading_type)
    headers.append('漢字')
    headers.append('index')
    if show_hyogai:
        for reading_type in ['呉音', '漢音', '宋唐音', '慣用音']:
            headers.append(reading_type + '_表外')
    if show_old_pron:
        for reading_type in ['呉音', '漢音', '宋唐音', '慣用音']:
            headers.append(reading_type + '_old')
    return headers


def output_ja_onyomi(args):
    """
    Deal with onyomi of ja
    """
    # get onyomi_dict
    kanji_yomi_dict, kanji_ydkey_map, all_onyomi_keys = parse_ja_yomi(args.input_wiki_cache_dir)
    
    # merge onyomi groups
    merged_onyomi_groups = generate_yomi_rows(kanji_yomi_dict, True, False, args.show_duplicated, args.merge_hyogai, args.show_hyogai)
    
    # Generate headers
    headers = generate_headers(args.show_duplicated, args.show_old_pron, args.show_hyogai)

    # output onyomi info
    output_yomi_info(
        merged_onyomi_groups, 
        filename=args.output_path, 
        output_format=args.output_format, 
        headers=headers,
    )
