import argparse
from preparation.args import regist_preparation
from wikt_cache.args import regist_wiktionary
from output.args import regist_parser

def cmdargs_parser():
    parser = argparse.ArgumentParser(description="Wiktionary Japanese and Chinese tools")

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Increase output verbosity"
    )
    sub_commands= parser.add_subparsers(dest='command', help='Available commands')
    
    # sub-command as key, list of functions as value
    # a sub-command: [sub-command-dealer functions list] dictionary will be returned after register_*() called
    function_register = {}
    
    # register sub-command: prepare
    function_register.update(regist_preparation(sub_commands))

    # register sub-command: wiktionary
    function_register.update(regist_wiktionary(sub_commands))

    # register sub-command: onyomi
    function_register.update(regist_parser(sub_commands))
    
    args = parser.parse_args()

    if args.verbose:
        print(f"Verbose mode enabled")
        
    if args.command not in function_register:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        exit(1)
        
    return args, function_register