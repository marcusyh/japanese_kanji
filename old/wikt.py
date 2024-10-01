from wiktionary.cache import WikiCache

# Object represent the wiktionry.org, and map it as a dictionary in local.


def parse_wikitext(wikitext):
    lines = wikitext.split('\n')
    result = {}
    stack = [result]  # 用一个栈来维护当前的嵌套字典结构

    for line in lines:
        if line.strip() == "":
            continue

        # check the level of header or sub header
        level = line.count('=') // 2
        title = line.strip('=').strip()

        if level > 0:
            # 通过栈的深度与标题等级判断，处理嵌套
            if level > len(stack):
                # 更深层的标题，继续嵌套
                new_dict = {}
                stack[-1][title] = new_dict
                stack.append(new_dict)
            else:
                # 返回到正确的层级，可能是相同层或者更高层的标题
                stack = stack[:level]
                new_dict = {}
                stack[-1][title] = new_dict
                stack.append(new_dict)
        else:
            # 非标题行，添加到最内层的字典中
            if "__content__" not in stack[-1]:
                stack[-1]["__content__"] = []
            stack[-1]["__content__"].append(line)

    return result


def get_ja_pronunciation():
    wc = WikiCache()
    wiki_dict = wc.wiki_dict()
    for kanji, item in wiki_dict.items():
        ja_text, zh_text_ja, zh_text_zh = item

```
'=={{L|ja}}==',
    '[[Category:{{ja}}|にゆう]]',
        '===={{pron}}====',
            '* 音読み   :',
                '** [[呉音]] : [[ニュウ]]（ニフ:[[入声]]であり無声子音の前では、「ニッ」となる）',
                '** [[漢音]] : [[ジュウ]]（ジフ）',
                '** [[慣用音]] : [[ジュ]]',
            '* 訓読み   : [[いる|い-る]]、[[いれる|い−れる]、][[はいる|はい-る]]､[[しお]]',
        '===={{prov}}====',
            '{{top}}',
            '*{{ふりがな|入会|yomi1=[[いりあい]]|yomi2=ニュウカイ|yomilink=n}}',
                '**[[入会権]]',
                '**[[入会地]]',
            '*{{ふりがな|入相|yomi1=[[いりあい]]|yomi2=ニュウショウ|yomilink=n}}',
            '*[[入口]]',
            '*[[入母屋]]',
            '*{{ふりがな|入魂|ジッコン|yomi2=ニュウコン|yomilink=n}}',
            '*{{ふりがな|入水|ジュスイ|yomi2=ニュウスイ|yomilink=n}}',
            '*[[入内]]',
            '*[[入声]]',
            '*[[入唐]]',
            '*[[入学]]',
            '*[[入管]]',
            '*[[入金]]',
            '*[[入室]]',
            '*[[入出]]',
            '*[[入籍]]',
            '*[[入道]]',
            '*[[入念]]',
            '*[[入門]]',
            '*[[入力]]',
            '*[[吸入]]',
            '*[[歳入]]',
            '*[[収入]]',
            '*{{ふりがな|一入|ひとしお}}',
            '{{bottom}}'
```

{
    '{{L|ja}}': {
        '__content__': ['[[Category:{{ja}}|にゆう]]'],
        '{{pron}}': {
            '__content__': [
                '* 音読み   :',
                '** [[呉音]] : [[ニュウ]]（ニフ:[[入声]]であり無声子音の前では、「ニッ」となる）',
                '** [[漢音]] : [[ジュウ]]（ジフ）',
                '** [[慣用音]] : [[ジュ]]',
                '* 訓読み   : [[いる|い-る]]、[[いれる|い−れる]、][[はいる|はい-る]]､[[しお]]'
            ],
            '{{prov}}': {
                '__content__': ['{{top}}']
            }
        }
    },
    '*{{ふりがな|入会|yomi1=[[いりあい]]|yomi2=ニュウカイ|yomilink=n}}': {
        '__content__': [
            '**[[入会権]]',
            '**[[入会地]]'
        ]
    },
    '*{{ふりがな|入相|yomi1=[[いりあい]]|yomi2=ニュウショウ|yomilink=n}}': {
        '__content__': [
            '*[[入口]]',
            '*[[入母屋]]'
        ]
    },
    '*{{ふりがな|入魂|ジッコン|yomi2=ニュウコン|yomilink=n}}': {},
    '*{{ふりがな|入水|ジュスイ|yomi2=ニュウスイ|yomilink=n}}': {
        '__content__': [
            '*[[入内]]',
            '*[[入声]]',
            '*[[入唐]]',
            '*[[入学]]',
            '*[[入管]]',
            '*[[入金]]',
            '*[[入室]]',
            '*[[入出]]',
            '*[[入籍]]',
            '*[[入道]]',
            '*[[入念]]',
            '*[[入門]]',
            '*[[入力]]',
            '*[[吸入]]',
            '*[[歳入]]',
            '*[[収入]]',
            '*{{ふりがな|一入|ひとしお}}',
            '{{bottom}}'
        ]
    }
}

