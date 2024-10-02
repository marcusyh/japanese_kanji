from commands import cmdargs_parser

if __name__ == '__main__':
    # get args and function_register from arg_parser
    args, funcs_register = cmdargs_parser()
    
    # execute the registered functions with args in registered order
    if args.command in funcs_register:
        func = funcs_register[args.command]
        func(args)