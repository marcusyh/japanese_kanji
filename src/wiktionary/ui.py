def confirm_fetch_list(current_cache_list, kanji_list, fetch_missing_only):
    cache_kanji_set = set(current_cache_list)
    local_kanji_set = set(kanji_list)

    missing_kanji_list = list(local_kanji_set - cache_kanji_set)
    all_kanji_list = list(local_kanji_set.union(cache_kanji_set))

    print(f'There are {len(kanji_list)} kanji in the preparation dictionary, which are the kanji to learn.')
    print(f'The Wiktionary cache file include {len(current_cache_list)} of them, {len(missing_kanji_list)} of them are missing.')
    
    if fetch_missing_only:
        message = f'Fetching missing {len(missing_kanji_list)} kanji only'
    else:
        message = f'Fetching all the definitions of these {len(all_kanji_list)} kanji'
        print(message)
        
    print("Do you want to check the list of kanji to fetch? (y/n)")
    response = input('(y/n): ').lower()
    if response in ['y', 'yes']:
        print(f'The list of kanji to fetch: {missing_kanji_list if fetch_missing_only else all_kanji_list}')
        
    return missing_kanji_list if fetch_missing_only else all_kanji_list


def confirm_fetch_remote(message):
    response = input(f'Now fetch these kanji from ja.wiktionary.org and zh.wiktionary.org? It maybe take many hours or many days depnends your network. (y/n): ').lower()
    if response not in ['y', 'yes']:
        print('Bye!')
        exit()

