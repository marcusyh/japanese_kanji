import os

ONYOMI_FILENAME = '日本語_音読み'
KUNYOMI_FILENAME = '日本語_訓読み'
WORDS_FILENAME = '日本語_単語'

OUTPUT_ROOT = '../data/parsed_result'

MARKDOWN_PATH = os.path.join(OUTPUT_ROOT, 'markdown')
CSV_PATH = os.path.join(OUTPUT_ROOT, 'csv')
HTML_PATH = os.path.join(OUTPUT_ROOT, 'html')

WIKT_CACHE_DIR = '../data/wiktionary'
WIKT_CACHE_FILE = os.path.join(WIKT_CACHE_DIR, 'cache.txt')
WIKT_PATCH_FILE = os.path.join(WIKT_CACHE_DIR, 'patch.txt')

PREPARATION_DIR = '../data/preparation'

WEBUI_DEPLOY_DIR = '/opt/japanese_kanji_yomi'