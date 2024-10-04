from preparation.utils import readfile

def deal_jinmei(source, appendix):
    """
    Creates a dictionary of kanji sets based on the input source and appendix.

    Args:
        source: A list of strings, where each string represents a row in the input file.
        appendix: A string to append to each kanji character.

    Returns:
        A dictionary where the keys are kanji sets and the values are empty dictionaries.
    """

    kanji_set = {}

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

def load_jinmei(data_root_dir, appendix = ''):
    """
    Returns:
        {
            '祢': {},
            '亘': {},
            '凜': {},
            ....
        }
    """
    return deal_jinmei(readfile(f'{data_root_dir}/じんめいじょうようかんじひょう'), appendix)