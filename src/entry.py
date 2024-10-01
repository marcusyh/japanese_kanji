from kanji_local import load_local_kanji
from wiktionary.cache import WikiCache
from commands import cmdargs_parser
from wiktionary.ja.japanese import parsing_ja
from wiktionary.ja.onyomi import process_onyomi

if __name__ == '__main__':
    #kanji_result, kanji_list = load_local_kanji()
    #print("Total kanji:", len(kanji_list))

    wc = WikiCache()
    
    pron_arch_all = parsing_ja(wc)

    process_onyomi(pron_arch_all)
    #wc.fetch(kanji_list)
    # get args and function_register from arg_parser
    args, funcs_register = cmdargs_parser()
    
    # execute the registered functions with args in registered order
    if args.command in funcs_register:
        func = funcs_register[args.command]
        func(args)