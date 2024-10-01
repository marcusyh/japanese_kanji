import argparse
from wiktionary.ja.args import add_onyomi_args
#from wiktionary.ja.kunyomi_args import register_kunyomi
#from wiktionary.zh.args import register_chinese

def cmdargs_parser():
    parser = argparse.ArgumentParser(description="Wiktionary Japanese and Chinese tools")

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Increase output verbosity"
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # sub-command as key, list of functions as value
    # a sub-command: [sub-command-dealer functions list] dictionary will be returned after register_*() called
    function_register = {}

    # register sub-command: onyomi
    function_register.update(add_onyomi_args(subparsers))
    
    # register sub-command: kunyomi
    #function_register.update(register_kunyomi(subparsers))

    # register sub-command: chinese
    #function_register.update(register_chinese(subparsers))

    args = parser.parse_args()

    if args.verbose:
        print(f"Verbose mode enabled")
        
    if args.command not in function_register:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        exit(1)
        
    return args, function_register