from wiktionary.ja.onyomi_parser import parse_onyomi
from wiktionary.ja.onyomi_formater import convert_to_merged_dict
from wiktionary.ja.onyomi_printer import print_all_kanji_info


def process_onyomi(pron_arch_all):
    onyomi = {}
    all_keys = {}
    for kanji, pron_arch in pron_arch_all.items():
        single = parse_onyomi(kanji, pron_arch)
        onyomi.update(single)
        
        for value in single.values():
            for key in value:
                all_keys[key] = all_keys.get(key, 0) + 1
                
    merged_dict = convert_to_merged_dict(onyomi, include_hyogai=False)
    print_all_kanji_info(merged_dict, show_old_pron=False)
    return onyomi, all_keys