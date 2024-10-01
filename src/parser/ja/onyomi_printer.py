from typing import Dict, List, Any
import inspect

def get_default_param(func, param_name, default_value):
    return inspect.signature(func).parameters.get(param_name, inspect.Parameter.empty).default or default_value


def generate_headers(show_old_pron, include_all_prons):
    headers = ["order", "all"] if include_all_prons else ["order"]
    for reading_type in ['呉音', '漢音', '慣用音', '宋唐音', '古音']:
        headers.append(reading_type)
        if show_old_pron:
            headers.append(reading_type + '_old')
    headers.append('漢字')
    return headers


def convert_to_rows(merged_kanji_info: List[Any], headers: List[str]) -> List[List[str]]:
    rows = []
    for idx, v in enumerate(merged_kanji_info):
        row = [str(idx+1)]
        for column in headers[1:]:
            if column in v:
                row.append('、'.join([p for p in v[column]]))
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



def print_all_kanji_info(
        merged_kanji_info: Dict[str, Any], 
        filename: str = None, 
        markdown_flag: bool = True, 
        show_old_pron: bool = True,
        include_all_prons: bool = False
    ):
    # Generate headers
    headers = generate_headers(show_old_pron, include_all_prons)
    
    # Process kanji data
    rows = convert_to_rows(merged_kanji_info, headers)
    
    # Format and output the result
    if markdown_flag:
        output = genrate_markdown(headers, rows, filename)
    else:
        output = genrate_csv(headers, rows, filename)
    
    if not filename:
        print(output)

    return output
