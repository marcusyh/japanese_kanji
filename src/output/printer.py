from typing import Dict, List, Any
import inspect
from file_util import prepare_output_path
from output.html_generator import generate_html

def get_default_param(func, param_name, default_value):
    return inspect.signature(func).parameters.get(param_name, inspect.Parameter.empty).default or default_value


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


def output_yomi_info(
        kanji_yomi_dict: Dict[str, Any],
        kanji_ydkey_map: Dict[str, Any],
        merged_kanji_info: Dict[str, Any], 
        filename: str = None, 
        output_format: str = 'markdown', 
        headers: List[str] = None,
    ):

    # Process kanji data
    rows = convert_to_rows(merged_kanji_info, headers)
    
    # Format and output the result
    if output_format == 'csv':
        genrate_csv(headers, rows, filename)
    elif output_format == 'markdown':
        genrate_markdown(headers, rows, filename)
    elif output_format == 'html':
        generate_html(filename, kanji_yomi_dict, kanji_ydkey_map)
        genrate_markdown(headers, rows, filename)
    else:
        raise ValueError(f'Invalid output format: {output_format}')