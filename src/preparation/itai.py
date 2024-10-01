from kanji.file_reader import readfile

def deal_itai(source, appendix):
    """
    This function processes a list of strings (source), appends a given appendix to each non-empty item,
    and stores the results in a dictionary with joined strings as keys and empty dictionaries as values.
    
    Parameters:
    source (list of str): The list of strings to process.
    appendix (str): The string to append to each item in the source list.
    
    Returns:
    dict: A dictionary with processed strings as keys and empty dictionaries as values.
    """
    
    kanji_set = {}
    
    # Iterate over each string in the source list
    for current in source:
        if current.strip() == '':
            continue
        items = current.strip().split(',')
        
        jis = []
        for ji in items:
            if not ji.strip():
                continue
            jis.append(ji.strip() + appendix)

        kanji_set['/'.join(jis)] = {}

    return kanji_set

def load_itai(appendix = ''):
    """
    Returns:
        {
            '亜/亞': {},
            '悪/惡': {},
            '為/爲': {},
            ....
        }
    """
    return deal_itai(readfile('kanji/いたいじ'), appendix)



if __name__ == '__main__':
    itai = load_itai()
