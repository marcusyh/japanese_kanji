from typing import Dict, List, Any
import inspect
from file_util import prepare_output_path

def get_default_param(func, param_name, default_value):
    return inspect.signature(func).parameters.get(param_name, inspect.Parameter.empty).default or default_value


def generate_headers(duplicate_by_all, show_old_pron, show_hyogai):
    headers = ["", "音序"] if duplicate_by_all else []
    for reading_type in ['呉音', '漢音', '宋唐音', '慣用音']:
        headers.append(reading_type)
    headers.append('漢字')
    headers.append('index')
    if show_hyogai:
        for reading_type in ['呉音', '漢音', '宋唐音', '慣用音']:
            headers.append(reading_type + '_表外')
    if show_old_pron:
        for reading_type in ['呉音', '漢音', '宋唐音', '慣用音']:
            headers.append(reading_type + '_old')
    return headers


def convert_to_rows(merged_kanji_info: List[Any], headers: List[str]) -> List[List[str]]:
    rows = []
    for raw_row in merged_kanji_info:
        row = []
        for column in headers:
            if column in ['index', '音序']:
                row.append(str(raw_row[column]))
            elif column == '':
                row.append('○' if raw_row['main_row_flag'] else '')
            elif column in raw_row:
                row.append('、'.join([p for p in raw_row[column]]))
            else:
                row.append('')
        rows.append(row)
    return rows


def genrate_markdown(headers, rows, filename):
    # makesure output path is valid and check if file exists
    prepare_output_path(filename)

    output = ['| ' + ' | '.join(headers) + ' |', '|' + '---|' * len(headers)]
    output.extend(['| ' + ' | '.join(row) + ' |' for row in rows])
    formatted_output = '\n'.join(output)
    
    if filename:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(formatted_output)
    
    return formatted_output


def genrate_csv(headers, rows, filename):
    # makesure output path is valid and check if file exists
    prepare_output_path(filename)

    output = [','.join(headers)]
    output.extend([','.join(row) for row in rows])
    formatted_output = '\n'.join(output)
    
    if filename:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(formatted_output)
    
    return formatted_output



def output_onyomi_info(
        merged_kanji_info: Dict[str, Any], 
        filename: str = None, 
        output_format: str = 'markdown', 
        show_duplicated: bool = False,
        show_old_pron: bool = True,
        show_hyogai: bool = False,
    ):
    # Generate headers
    headers = generate_headers(show_duplicated, show_old_pron, show_hyogai)
    
    # Process kanji data
    rows = convert_to_rows(merged_kanji_info, headers)
    
    # Format and output the result
    if output_format == 'csv':
        genrate_csv(headers, rows, filename)
    else:
        genrate_markdown(headers, rows, filename)
