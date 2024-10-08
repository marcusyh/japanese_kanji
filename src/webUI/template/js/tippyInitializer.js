import { generateKanjiContent, mergeKanjiInfo } from './kanjiProcessor.js';

export function initializeTippy(kanjiInfo) {
    console.time('initializeTippy');
    console.log("Initializing Tippy with kanjiInfo:", Object.keys(kanjiInfo).length);
    if (typeof tippy === 'function') {
        const kanjiElements = document.querySelectorAll('.kanji');
        kanjiElements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                if (!element._tippy) {
                    tippy(element, {
                        content: '加载中...',
                        allowHTML: true,
                        onShow(instance) {
                            const fullText = instance.reference.dataset.kanji;
                            const validKanji = fullText.split('').filter(char => kanjiInfo.hasOwnProperty(char));
                            
                            if (validKanji.length === 0) {
                                instance.setContent(`没有找到有效的汉字信息`);
                                return;
                            }

                            if (validKanji.length === 1) {
                                const info = kanjiInfo[validKanji[0]];
                                instance.setContent(generateKanjiContent(validKanji[0], info));
                            } else {
                                const mergedInfo = mergeKanjiInfo(validKanji.map(k => ({ kanji: k, info: kanjiInfo[k] })));
                                let content = '';
                                mergedInfo.forEach(group => {
                                    content += generateKanjiContent(group.kanji.join(''), group.info);
                                });
                                instance.setContent(content);
                            }
                        },
                        maxWidth: 500,
                        interactive: true,
                        appendTo: () => document.body,
                    });
                }
                element._tippy.show();
            });
        });
        console.log("Tippy initialized for kanji elements");
    } else {
        console.error('Tippy.js is not loaded correctly');
    }
    console.timeEnd('initializeTippy');
}
