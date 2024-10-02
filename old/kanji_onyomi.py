from source.read_jouyou import read_jouyou
from source.read_jinmei import read_jinmei
from source.read_hougai import read_hougai
from source.read_itai import read_itai



def merge_kanji():
    jouyou = read_jouyou()
    jinmei = read_jinmei()
    hougai = read_hougai()
    itai = read_itai()

from old.classify_data import get_classified, add_alter
from save_file import save_to_docx, save_to_csv


FILENAME = '常用汉字列表音読み'
FILEPATH = '/tmp'


if __name__ == '__main__':
    hira, kata = get_classified(jouyou, jinmei, hougai)
    kata, remains = add_alter(kata)

    save_to_docx(kata, FILENAME, FILEPATH)
