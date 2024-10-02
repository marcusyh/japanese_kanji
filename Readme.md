# Japanese Kanji Pronunciation Classifier

## Description

This project fetches kanji from ja.wiktionary.org, organizes their onyomi (Chinese-derived readings), and attempts to present them in a clear order for learners. It is primarily targeted towards East Asian language speakers who are familiar with kanji characters but may not know their Japanese pronunciations.

## Limitations

1. This tool relies on web scraping and may be affected by changes to the structure of ja.wiktionary.org. Due to inconsistencies and exceptions in the source data, manual adjustments and hardcoded rules are employed. For optimal performance, download all code and data together. Compatibility with future versions of Wiktionary is not guaranteed.

2. This tool is still under development and may have limited functionality.

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
This sub-command fetches or updates the `data/wiktionary/cache.txt` file. It fetches data from both `ja.wiktionary.org` and `zh.wiktionary.org` for each kanji. 
Each kanji in `data/wiktionary/cache.txt` is on a single line. It contains tab-separated information in 3 fields. The first field is the kanji itself. The second field is information fetched from `ja.wiktionary.org`, and the third field is from zh.wiktionary.org.

#### `parse`
The `parse` sub-command has its own sub-level commands. It's used to parse the fetched `wiktionary/cache.txt`. It's not finished yet. There is only an `onyomi` sub-sub-command available now. 
- `onyomi`: parses `data/wiktionary/cache.txt` and generates a table of onyomi for all the Japanese kanji. The output format can be markdown or CSV.