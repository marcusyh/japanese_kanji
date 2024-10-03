
from wikt_parser import parse_ja_onyomi
from output.ja_onyomi.formater import merge_onyomi_groups
from output.ja_onyomi.printer import output_onyomi_info


def output_ja_onyomi(args):
    """
    Deal with onyomi of ja
    """
    # get onyomi_dict
    onyomi_dict, all_onyomi_keys = parse_ja_onyomi(args.wiki_cache_dir)

    # merge onyomi groups
    merged_onyomi_groups = merge_onyomi_groups(onyomi_dict, args.include_hyogai, args.include_all_prons)

    # output onyomi info
    output_onyomi_info(
        merged_onyomi_groups, 
        filename=args.filepath, 
        markdown_flag=args.is_markdown, 
        show_old_pron=args.show_old_pron, 
        include_all_prons=args.include_all_prons
    )