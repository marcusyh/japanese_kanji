import { generateKanjiContent } from './kanjiProcessor.js';

export function initializeTippy(kanjiInfo) {
    console.log("Initializing Tippy with kanjiInfo:", Object.keys(kanjiInfo).length);
    if (typeof tippy === 'function') {
        const elements = document.querySelectorAll('#table-container .kanji');
        //console.log("Found .kanji elements:", elements.length);
        const instances = tippy('#table-container .kanji', {
            content: '加载中...',
            allowHTML: true,
            onShow(instance) {
                try {
                    const fetchedString = instance.reference.textContent;
                    const validKanji = fetchedString.split('').filter(char => kanjiInfo.hasOwnProperty(char));

                    if (validKanji.length === 0) {
                        instance.setContent(`没有找到有效的汉字信息`);
                        return;
                    }

                    let content = '';
                    validKanji.forEach(kanji => {
                        const info = kanjiInfo[kanji];
                        if (info) {
                            content += generateKanjiContent(kanji, info);
                        } else {
                            content += `<div class="kanji-info"><h3>${kanji}</h3><p>没有找到信息</p></div>`;
                        }
                    });
                    instance.setContent(content);
                } catch (error) {
                    console.error('Error in Tippy onShow:', error);
                    instance.setContent('加载信息时发生错误');
                }
            },
            maxWidth: 500,
            interactive: true,
            appendTo: () => document.body
        });
        console.log("Created Tippy instances:", instances.length);
    } else {
        console.error('Tippy.js is not loaded correctly');
    }
}
