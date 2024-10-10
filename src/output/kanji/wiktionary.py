import os
import re
import json
from file_util import prepare_file_path

def update_html_text(raw_text, language):
    # Remove HTML comments (including multi-line comments)
    html_text = re.sub(r'<!--[\s\S]*?-->', '', raw_text)
    
    # Remove "edit" sections
    html_text = re.sub(r'\[<\/span><a\s+href="[^"]*"\s+title="[^"]*"><span>[^<]*<\/span><\/a><span[^>]*>\]', '', html_text)
    
    # Convert relative URLs to absolute URLs and add target="_blank"
    base_url = f"https://{language}.wiktionary.org"
    html_text = re.sub(r'<a\s+href="(/[^"]*)"', f'<a href="{base_url}\\1" target="_blank"', html_text)
    
    # Add target="_blank" to absolute URLs
    html_text = re.sub(r'<a\s+href="(https?://[^"]*)"', r'<a href="\1" target="_blank"', html_text)
    
    return html_text


def update_html_file(src_path, dst_path):
    with open(src_path, 'r', encoding='utf-8') as src_file:
        html_dict = json.load(src_file)
    
    html_text = ''
    if 'ja' in html_dict and html_dict['ja']:
        ja_html  = update_html_text(html_dict['ja'], 'ja')
        html_text += f'{ja_html}\n<br>\n'

    if 'zh1' in html_dict and html_dict['zh1']:
        zh_html1 = update_html_text(html_dict['zh1'], 'zh')
        html_text += f'{zh_html1}\n<br>\n'

    if 'zh2' in html_dict and html_dict['zh2']:
        zh_html2 = update_html_text(html_dict['zh2'], 'zh')
        html_text += f'{zh_html2}\n<br>\n'

    with open(dst_path, 'w', encoding='utf-8') as dst_file:
        dst_file.write(html_text)


def convert_wikt_to_html(src_dir, dst_dir):
    prepare_file_path(dst_dir, is_dir=True, create_if_not_exists=True, delete_if_exists=True)

    for filename in sorted(os.listdir(src_dir)):
        file_base_name = os.path.splitext(filename)[0]
        src_file_path = os.path.join(src_dir, filename)
        dst_file_path = os.path.join(dst_dir, f'{file_base_name}.html')
        update_html_file(src_file_path, dst_file_path)