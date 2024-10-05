
from wikt_parser import parse_ja_yomi
from output.ja_onyomi.formater import generate_onyomi_rows
from output.ja_onyomi.printer import output_onyomi_info
from output.html_generator import generate_html


def output_ja_onyomi(args):
    """
    Deal with onyomi of ja
    """
    # get onyomi_dict
    kanji_yomi_dict, kanji_ydkey_map, all_onyomi_keys = parse_ja_yomi(args.input_wiki_cache_dir)
    
    # merge onyomi groups
    merged_onyomi_groups = generate_onyomi_rows(kanji_yomi_dict, args.merge_hyogai, args.show_hyogai, args.show_duplicated)

    # if output format is html, generate html file
    output_format = args.output_format
    if args.output_format == 'html':
        generate_html(args.output_path, kanji_yomi_dict, kanji_ydkey_map)
        output_format = 'markdown'

    # output onyomi info
    output_onyomi_info(
        merged_onyomi_groups, 
        filename=args.output_path, 
        output_format=output_format, 
        show_duplicated=args.show_duplicated,
        show_old_pron=args.show_old_pron, 
        show_hyogai=args.show_hyogai,
    )