
from wikt_parser import parse_ja_onyomi
from output.ja_onyomi.formater import generate_onyomi_rows
from output.ja_onyomi.printer import output_onyomi_info


def output_ja_onyomi(args):
    """
    Deal with onyomi of ja
    """
    # get onyomi_dict
    onyomi_dict, all_onyomi_keys = parse_ja_onyomi(args.wiki_cache_dir)

    # merge onyomi groups
    merged_onyomi_groups = generate_onyomi_rows(onyomi_dict, args.include_hyogai, args.duplicate_by_all)

    # output onyomi info
    output_onyomi_info(
        merged_onyomi_groups, 
        filename=args.filepath, 
        csv_flag=args.is_csv, 
        show_old_pron=args.show_old_pron, 
        duplicate_by_all=args.duplicate_by_all
    )