from typing import Dict, List, Any
import inspect
from file_util import prepare_output_path

def get_default_param(func, param_name, default_value):
    return inspect.signature(func).parameters.get(param_name, inspect.Parameter.empty).default or default_value


def generate_headers(show_old_pron, include_all_prons):
    headers = ["onyomi"] if include_all_prons else []
    for reading_type in ['呉音', '漢音', '慣用音', '宋唐音', '古音']:
        headers.append(reading_type)
        if show_old_pron:
            headers.append(reading_type + '_old')
    headers.append('漢字')
    headers.append('index')
    return headers


def convert_to_rows(merged_kanji_info: List[Any], headers: List[str]) -> List[List[str]]:
    rows = []
    for raw_row in merged_kanji_info:
        row = []
        for column in headers:
            if column in ['index', 'onyomi']:
                row.append(str(raw_row[column]))
            elif column in raw_row:
                row.append('、'.join([p for p in raw_row[column]]))
            else:
                row.append('')
        rows.append(row)
    return rows


def genrate_markdown(headers, rows, filename):
    output = ['| ' + ' | '.join(headers) + ' |', '|' + '---|' * len(headers)]
    output.extend(['| ' + ' | '.join(row) + ' |' for row in rows])
    formatted_output = '\n'.join(output)
    
    if filename:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(formatted_output)
    
    return formatted_output


def genrate_csv(headers, rows, filename):
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
        csv_flag: bool = False, 
        show_old_pron: bool = True,
        duplicate_by_all: bool = False
    ):
    # makesure output path is valid and check if file exists
    prepare_output_path(filename)

    # Generate headers
    headers = generate_headers(show_old_pron, duplicate_by_all)
    
    # Process kanji data
    rows = convert_to_rows(merged_kanji_info, headers)
    
    # Format and output the result
    if csv_flag:
        output = genrate_csv(headers, rows, filename)
    else:
        output = genrate_markdown(headers, rows, filename)
    
    if not filename:
        print(output)

    return output
