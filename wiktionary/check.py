import os 
import wikitextparser as wtp

def print_by_sections(kanji, parsed_wikitext):
    #os.system('clear')

    print('==================================== %s start ====================================\n\n' %kanji)
    for x in parsed_wikitext.sections[2:]:
        print(x)
    print('====================================  %s End  ====================================\n\n\n\n\n\n' %kanji)

    #input('Please press Enter key to continue ...')

 
def check_sections(wiki_parsed):
    counts = [0, 0, 0]
    failed = {}
    # total, normal, inormal
    for k, v in wiki_parsed.items():
        counts[0] += 1
        if v.sections[0].string == '' and v.sections[1].string == v.string:
            counts[1] += 1
            continue
        else:
            counts[2] += 1
            failed[k] = v

    print('Wikitext sections check finished, %s wikinode in total, %s have normal section structure, %s failed\n' %tuple(counts))

    if counts[2] != 0:
        for k, v in failed.items():
            #os.system('clear')
            print_by_sections(k, v)
 
def check_youmi(wiki_parsed):
    # prepare
    counts = {}
    for k, v in wiki_parsed.items():
        location = 1
        counts[k] = {3:[], 2:[], 1: [], 0:[]}
        for x in v.sections[2:]:
            location += 1
            if x.string.find('音読み') >=0 and x.string.find('訓読み') >= 0:
                counts[k][3].append(location) 
                continue
            if x.string.find('音読み') >=0:
                counts[k][2].append(location)
                continue
            if x.string.find('訓読み') >= 0:
                counts[k][1].append(location)
                continue
            counts[k][0].append(location)
     
    cnt_error = {} # Kanjis which have more than 1 kind of pattern
    cnt_align = {} # Kanjis which have one kind of pattern, but the youmi is not located at position 2.
    cnt_normal = {1: [], 2: [], 3: []}
    for k, v in counts.items():
        if len(v[3]) + len(v[2]) + len(v[1]) != 1:
            cnt_error[k] = v
            continue
        if v[3] + v[2] + v[1] != [2]:
            cnt_align[k] = v
            continue
        for idx in [1, 2, 3]:
            if v[idx] == [2]:
                cnt_normal[idx].append(k)
                break

    def print_index(k, v):
        print("\tKanji %s: 音読み and 訓読み index are %s, 音読み index are %s, 訓読み index are %s," %(k, ', '.join([str(x) for x in v[3]]), ', '.join([str(x) for x in v[2]]), ', '.join([str(x) for x in v[1]])))

    print('Wikitext youmi check finished, %s wikinode in total, %s have normal youmi, %s have a not aligned youmi, %s have some error\n' %(len(counts), len(counts) - len(cnt_align) - len(cnt_error), len(cnt_align), len(cnt_error)))

    if len(cnt_error) != 0:
        print("The error kanji list: ")
        for k, v in cnt_error.items():
            print_index(k, v)

    if len(cnt_align) != 0:
        print("The location of some youmi is not located at position 2:")
        for k, v in cnt_align.items():
            print_index(k, v)

    for k, v in cnt_error.items():
        print_index(k, v)
        print_by_sections(k, wiki_parsed[k])

    for k, v in cnt_align.items():
        print_index(k, v)
        print_by_sections(k, wiki_parsed[k])


    print("\nThe %s normal can be classified as follow:" %sum([len(x) for k, x in cnt_normal.items()]))
    print("\t%s have both 音読み and 訓読み" %len(cnt_normal[3]))
    print("\t%s have only 音読み" %len(cnt_normal[2]))
    print("\t%s have only 訓読み" %len(cnt_normal[1]))
            
            
def check_wikt(wiki_dict):
    wiki_parsed = {k: wtp.parse(v) for k, v in wiki_dict.items()}
    check_sections(wiki_parsed)
    check_youmi(wiki_parsed)
