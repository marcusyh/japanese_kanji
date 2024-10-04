
from wikt_parser import parse_ja_onyomi
from output.ja_onyomi.formater import generate_onyomi_rows
from output.ja_onyomi.printer import output_onyomi_info


def output_ja_onyomi(args):
    """
    Deal with onyomi of ja
    """
    # get onyomi_dict
    onyomi_dict, all_onyomi_keys = parse_ja_onyomi(args.input_wiki_cache_dir)
    for kanji, info in onyomi_dict.items():
        if '古音' not in info:
            continue
        print(kanji, info)

    # merge onyomi groups
    merged_onyomi_groups = generate_onyomi_rows(onyomi_dict, args.merge_hyogai, args.show_hyogai, args.show_duplicated)

    # output onyomi info
    output_onyomi_info(
        merged_onyomi_groups, 
        filename=args.output_filepath, 
        csv_flag=args.output_is_csv, 
        show_duplicated=args.show_duplicated,
        show_old_pron=args.show_old_pron, 
        show_hyogai=args.show_hyogai,
    )