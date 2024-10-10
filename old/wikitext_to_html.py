import re
import os
from html import escape
import mwparserfromhell
from wikt_cache.wiki_cache import WikiCache
from file_util import prepare_file_path

def custom_template_handler(template):
    """自定义模板处理函数"""
    name = str(template.name).strip().lower()
    if name in ['ja', 'zh', 'noun', 'prov', 'suffix']:
        return f'<span class="template {name}">{template}</span>'
    elif name == 'pagename':
        return '{{PAGENAME}}'  # 保留原样，后续可能需要特殊处理
    elif name == 'trans_link':
        # 处理 trans_link 模板
        params = template.params
        if len(params) >= 2:
            lang = str(params[0]).strip()
            text = str(params[1]).strip()
            return f'<span class="trans_link" lang="{lang}">{text}</span>'
    elif name == 'pron':
        # 处理 pron 模板
        params = template.params
        if len(params) >= 1:
            lang = str(params[0]).strip()
            return f'<span class="pron" lang="{lang}">[pronunciation]</span>'
    return str(template)

def custom_link_handler(target, text=None):
    """自定义链接处理函数"""
    if text is None:
        text = target
    return f'<a href="#{target}">{text}</a>'

def custom_post_processing(html):
    """自定义后处理函数"""
    # 处理连续的换行符
    html = re.sub(r'\n{2,}', '</p><p>', html)
    
    # 处理列表（确保不会影响已经转换的 HTML）
    html = re.sub(r'(?<!<li>)\*\s', '<ul><li>', html)
    html = re.sub(r'(?<!<li>)#\s', '<ol><li>', html)
    html = re.sub(r'</li>\s*(?=[*#])', '</li><li>', html)
    html = re.sub(r'</li>\s*(?!</?[uo]l>)', '</li></ul>', html)
    
    # 处理其他特殊情况
    html = html.replace('&lt;sup&gt;', '<sup>').replace('&lt;/sup&gt;', '</sup>')
    
    # 处理 {{PAGENAME}}
    html = html.replace('{{PAGENAME}}', '<span class="pagename">[current page name]</span>')
    
    # 合并单行的、没有HTML标签的词语
    lines = html.split('\n')
    merged_lines = []
    buffer = []
    in_reading_section = False
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('音読み') or stripped_line.startswith('訓読み'):
            in_reading_section = True
        if stripped_line.startswith('<p>') and not in_reading_section:
            in_reading_section = False
        
        if stripped_line and not re.search(r'<[^>]+>', stripped_line) and not in_reading_section:
            buffer.append(stripped_line)
        else:
            if buffer:
                merged_lines.append('<p>' + '、'.join(buffer) + '</p>')
                buffer = []
            if stripped_line:
                merged_lines.append(line)
    if buffer:
        merged_lines.append('<p>' + '、'.join(buffer) + '</p>')
    
    html = '\n'.join(merged_lines)
    
    # 移除多余的空段落
    html = re.sub(r'<p>\s*</p>', '', html)
    
    # 确保整个内容被包裹在段落标签中
    if not html.startswith('<p>'):
        html = f'<p>{html}'
    if not html.endswith('</p>'):
        html = f'{html}</p>'
    
    return html

def convert_to_html(wikitext):
    # 解析 wikitext
    parsed = mwparserfromhell.parse(wikitext)
    
    # 自定义处理
    for node in parsed.ifilter_templates():
        replacement = custom_template_handler(node)
        if replacement != str(node):
            parsed.replace(node, replacement)
    
    # 将解析后的内容转换为字符串
    html = str(parsed)
    
    # 处理 Wikilinks
    html = re.sub(r'\[\[([^|]+?)\]\]', lambda m: custom_link_handler(m.group(1)), html)
    html = re.sub(r'\[\[([^|]+?)\|([^\]]+?)\]\]', lambda m: custom_link_handler(m.group(1), m.group(2)), html)
    
    # 转换为 HTML
    html = mwparserfromhell.parse(html).strip_code()
    
    # 后处理
    html = custom_post_processing(html)
    
    return html

def save_html_file(output_dir, kanji, details_texts):
    if len(details_texts) == 0:
        return
    
    html_parts = []
    for details_text in details_texts:
        html_part = convert_to_html(details_text)
        html_parts.append(html_part)
    
    html = '<hr>'.join(html_parts)
    
    file_path = os.path.join(output_dir, f'{kanji}.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

def convert_wikt_to_html(wiki_cache_dir, output_dir):
    wiki_cache = WikiCache(wiki_cache_dir)

    prepare_file_path(output_dir, is_dir=True, delete_if_exists=True, create_if_not_exists=True)

    for kanji, details_texts in wiki_cache.wiki_dict.items():
        save_html_file(output_dir, kanji, details_texts)

