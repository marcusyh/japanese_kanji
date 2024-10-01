from kanji.file_reader import readfile

def deal_weblio(source, appendix):
    """
    Creates a dictionary of kanji and their sounds from a Weblio source.
    
    Args:
        source: A list of strings, each containing a line from the Weblio source.
        appendix: A string to append to the kanji readings.

    Returns:
        A dictionary with kanji as keys and a dictionary of sounds as values.
    """

    kanji_set = {}
    
    for current in source:
        if current == '':
            continue
        items = current.split(',')
        sound = items[0].strip()
        
        jis = []
        for ji in items[1:]:
            if not ji.strip():
                continue
            jis.append(ji.strip() + appendix)

        kanji_set['/'.join(jis)] = {sound: ''}

    return kanji_set

def load_hyougai(appendix = ''):
    """
    Returns: 
        {
        '穎/頴': {'エイ': ''},
        '蛙': {'ア': ''},
        ...
    """
    return deal_weblio(readfile('kanji/ひょうがいかんじじたいひょう'), appendix)

if __name__ == '__main__':
    hougai = load_hyougai()
