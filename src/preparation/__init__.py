from preparation.loader import load_local_kanji, load_local_kanji_without_tag
from file_util import convert_to_writable, save_to_docx, save_to_csv

def prepare_kanji_data(args, **kanji_types):
    # get kanji data from loader
    kanji_result, kanji_list = load_local_kanji(**kanji_types, with_tag=args.with_tag, data_root_dir=args.source_data_dir)

    # convert to writable format
    wrtb = convert_to_writable(kanji_result)

    if args.format == 'csv':
        save_to_csv(wrtb, args.output_file_path)
    elif args.format == 'docx':
        save_to_docx(wrtb, 'test.docx', '漢字の音読み', '/tmp/')
