
from parser.ja_general import parse_ja
from parser.ja_onyomi.parser import parse_onyomi
from parser.ja_onyomi.formater import merge_onyomi_groups
from parser.ja_onyomi.printer import output_onyomi_info


def process_ja_onyomi(args):
    """
    Deal with onyomi of ja
    """
    # get pron_arch_dict
    pron_arch_dict = parse_ja(args.wiki_cache_dir)

    # parse onyomi of ja
    onyomi_dict, all_onyomi_keys = parse_onyomi(pron_arch_dict)

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