# Japanese Kanji Pronunciation Classifier

## Description

This project fetches kanji from ja.wiktionary.org, organizes their onyomi (Chinese-derived readings), and attempts to present them in a clear order for learners. It is primarily targeted towards East Asian language speakers who are familiar with kanji characters but may not know their Japanese pronunciations.

## Limitations

1. This tool relies on web scraping and may be affected by changes to the structure of ja.wiktionary.org. Due to inconsistencies and exceptions in the source data, manual adjustments and hardcoded rules are employed. For optimal performance, download all code and data together. Compatibility with future versions of Wiktionary is not guaranteed.

2. There are numerous arguments for these sub-commands, many of which have not been thoroughly tested. As a result, bugs may be present.

## Usage
As this tool is partly finished, here's how to use it:
- Clone this repository
- Install required packages by running `pip install -r requirements.txt`
- Navigate to the `src` directory
- Run `python entry sub-command`, you may use `python entry -h` to check the details
- There are 3 sub-commands available at the current time

## Sub-commands
#### `prepare`
The `prepare` sub-command is located in `src/preparation`. It parses manually placed files in `data/preparation`. It can be used to generate a CSV or DOCX file using the information inside `data/preparation`. It also generates a list of kanji which is used to fetch definitions from Wiktionary.

#### `wikt`
This sub-command fetches or updates the `data/wiktionary/cache.txt` file and `data/wiktionary/html/*.json`. It fetches data from both `ja.wiktionary.org` and `zh.wiktionary.org` for each kanji. 
- `-c`
    This argument is used to update `data/wiktionary/cache.txt`. Each kanji in this file is on a single line. It contains tab-separated information in 4 fields. The first field is the kanji itself. The second and third fields contain information fetched from `ja.wiktionary.org`, and the last field is from `zh.wiktionary.org`.
- `-ht`
    This argument is used to update `data/wiktionary/html`

#### `parse`
The `parse` sub-command has its own sub-level commands. It's used to parse the fetched `wiktionary/cache.txt`. 
- `onyomi`: parses `data/wiktionary/cache.txt` and `data/preparation`, merges the data from the two sources, and generates a table of onyomi for all the Japanese kanji. The output format can be markdown or CSV.
- `kunyomi`: parses `data/preparation` and generates a table of kunyomi for all the Japanese kanji. The output format can be markdown or CSV.
- `kanji`: parses `data/wiktionary/cache.txt` and `data/preparation` to generate additional info for each kanji.

#### `webui`
- This sub-command copies a simple Python HTTP server, the web JS/HTML/CSS files, and the markdown file/kanji additional info files to `/opt/japanese_kanji_yomi`. For details, please refer to `python entry.py webui -h`