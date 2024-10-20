import os

################################
# preparation
################################
PREPARATION_DIR = '../data/preparation'


################################
# wiktionary
################################
WIKT_CACHE_DIR = '../data/wiktionary'
WIKT_CACHE_FILE = os.path.join(WIKT_CACHE_DIR, 'cache.txt')
WIKT_PATCH_FILE = os.path.join(WIKT_CACHE_DIR, 'patch.txt')
WIKT_HTML_DIR = os.path.join(WIKT_CACHE_DIR, 'html')


################################
# output
################################
OUTPUT_ROOT = '../data/parsed_result'

MARKDOWN_PATH = os.path.join(OUTPUT_ROOT, 'markdown')
CSV_PATH = os.path.join(OUTPUT_ROOT, 'csv')
HTML_PATH = os.path.join(OUTPUT_ROOT, 'html')

ONYOMI_FILENAME = '日本語_音読み'
KUNYOMI_FILENAME = '日本語_訓読み'
WORDS_FILENAME = '日本語_単語'


################################
# learning
################################
LEARNING_DIR = '../data/learning'


################################
# webUI
################################
WEBUI_DEPLOY_DIR = '/opt/japanese_kanji_yomi'


################################
# ja_web
################################
JA_WEB_DEPLOY_DIR = '../../ja_web'