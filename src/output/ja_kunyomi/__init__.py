
from wikt_parser import parse_ja_yomi
from output.formater import generate_yomi_rows
from output.yomi_printer import output_yomi_info

def generate_headers(duplicate_by_all):
    headers = ["", "音序"] if duplicate_by_all else []
    for reading_type in ['訓読み', '漢字', 'index']:
        headers.append(reading_type)
    return headers


def output_ja_kunyomi(args):
    """
    Deal with kunyomi of ja
    """
    # get kunyomi_dict
    kanji_yomi_dict, kanji_ydkey_map, all_kunyomi_keys = parse_ja_yomi(args.input_wiki_cache_dir)
    
    # merge kunyomi groups
    merged_kunyomi_groups = generate_yomi_rows(kanji_yomi_dict, False, True, args.show_duplicated)
    
    # Generate headers
    headers = generate_headers(args.show_duplicated)

    # output kunyomi info
    output_yomi_info(
        merged_kunyomi_groups, 
        filename=args.output_path, 
        output_format=args.output_format, 
        headers=headers,
    )
