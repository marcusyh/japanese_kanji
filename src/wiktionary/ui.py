def wait_for_user_input(message):
    while True:
        print(message)
        response = input('').lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print('Please enter y or n')


def show_brief_info(local_count, cache_count, missing_count, fetch_missing_only):
    print(f'There are {local_count} kanji in the preparation dictionary, which are the kanji to learn.')
    print(f'The Wiktionary cache file include {cache_count} of them, {missing_count} of them are missing.')
    
    if fetch_missing_only:
        message = f'Fetching missing {missing_count} kanji only'
    else:
        message = f'Fetching all the definitions of these {local_count} kanji'
    print(message)

        
def show_kanji_list(missing_kanji_list, update_kanji_list, fetch_missing_only):
    check_kanji_msg = f'Do you want to check the list of kanji to fetch? (y/n)'
    if not wait_for_user_input(check_kanji_msg):
        return False

    print(f'The list of kanji to fetch: {missing_kanji_list}')
    if not fetch_missing_only:
        print(f'The list of kanji to update: {update_kanji_list}')

    return True


def confirm_fetch_remote():
    confirm_msg = f'Now fetch these kanji from ja.wiktionary.org and zh.wiktionary.org? It maybe take many hours or many days depnends your network. (y/n): '
    if not wait_for_user_input(confirm_msg):
        exit()
    return True