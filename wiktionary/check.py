import os 
import wikitextparser as wtp

def print_by_sections(parsed_wikitext):
    os.system('clear')
    for x in parsed_wikitext.sections[2:]:
        print('------%s start-----\t' %k, x, '\t-----%s end------\n\n\n' %k)
    input('Please press Enter key to continue ...')
 
def check_sections(pared_wikitext):
    counts = [0, 0, 0]
    for k, v in wiki_parsed.items():
        counts[0] += 1
        if v.sections[0].string == '' and v.sections[1].string == v.string:
            counts[1] += 1
            continue
        else:
            counts[2] += 1

    print('Wikitext sections check finished, %s wikinode in total, %s have normal section structure, %s failed\n' %tuple(counts))

    if counts[2] != 0:
        input('Press Enter to check the failed')
        for 
 

wiki_parsed = {k: wtp.parse(v) for k, v in wiki_dict}
    
   os.system('clear')
    for x in v.sections:
        print('------%s start-----\t' %k, x, '\t-----%s end------\n\n\n' %k)
    input()
 

counts = {}

for k, v in wiki_parsed.items():
    sum = 0
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
 


for k, v in counts.items():
    if len(v[3]) + len(v[2]) + len(v[1]) != 1:
        print(k)
        

for k, v in counts.items():
    if len(v[3]) + len(v[2]) + len(v[1]) != 1:
        print(k, v)
        
        

for k, v in counts.items():
    if len(v[3]) + len(v[2]) + len(v[1]) != 1:
        continue
    if v[3] + v[2] + v[1] != [2]:
        print(k, v)
        
        
        

suma = {3: {}, 2:{}, 1: {}, 0: {}}

for k1, v1  in counts.items():
    for k2, v2 in v1.items():
        for k3 in v2:
            if k3 not in suma[k2]:
                suma[k2][k3] = []
            suma[k2][k3].append(k1)
            

suma.keys()
for a, b in suma.items():
    print(a, len(b))
    

for a, b in suma.items():
    for x, y in b.items():
        print(a, x, len(y))
        
    

for a, b in suma.items():
    for x, y in b.items():
        if a == 0 or x == 2:
            continue
        print(a, x, len(y))
        
        
    

for a, b in suma.items():
    for x, y in b.items():
        if a == 0 or x == 2:
            continue
        for i in y:
            ps(wiki_parsed[i])
                    
        
    

