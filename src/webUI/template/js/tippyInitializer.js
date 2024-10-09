import { generateKanjiContent, mergeKanjiInfo, fetchWiktContent } from './kanjiProcessor.js';

const state = {
    wiktFiles: {},
    activeTooltip: null,
    isWiktButtonClicked: false,
    mouseLeaveTimer: null
};

const config = {
    mouseLeaveDelay: 300,
    minTooltipWidth: 0.05,
    maxTooltipWidth: 0.4
};

async function loadWiktFiles() {
    const response = await fetch('/wikt_files');
    state.wiktFiles = await response.json();
}

function calculateTooltipWidth(content) {
    const dummyElement = document.createElement('div');
    dummyElement.style.cssText = 'visibility: hidden; position: absolute; white-space: nowrap;';
    dummyElement.innerHTML = content;
    document.body.appendChild(dummyElement);

    const contentWidth = dummyElement.offsetWidth;
    document.body.removeChild(dummyElement);

    const viewportWidth = window.innerWidth;
    const minWidth = viewportWidth * config.minTooltipWidth;
    const maxWidth = viewportWidth * config.maxTooltipWidth;

    return Math.min(Math.max(contentWidth, minWidth), maxWidth);
}

async function createTooltipContent(validKanji, kanjiInfo) {
    let content = '';
    if (validKanji.length === 1) {
        const info = kanjiInfo[validKanji[0]];
        content = generateKanjiContent(validKanji[0], info);
    } else {
        const mergedInfo = mergeKanjiInfo(validKanji.map(k => ({ kanji: k, info: kanjiInfo[k] })));
        mergedInfo.forEach(group => {
            content += generateKanjiContent(group.kanji.join(''), group.info);
        });
    }

    for (const kanji of validKanji) {
        if (state.wiktFiles[kanji]) {
            try {
                const wiktContent = await fetchWiktContent(state.wiktFiles[kanji]);
                if (wiktContent && wiktContent.trim() !== '') {
                    content += `
                        <div class="wikt-content-wrapper">
                            <button class="wikt-toggle" data-kanji="${kanji}">显示维基词典内容</button>
                            <div class="wikt-content" style="display:none;"></div>
                        </div>
                    `;
                }
            } catch (error) {
                console.error(`Error fetching Wiktionary content for ${kanji}:`, error);
            }
        }
    }

    return content;
}

function handleWiktButtonClick(e) {
    e.stopPropagation();
    e.preventDefault();
    state.isWiktButtonClicked = true;
    const content = e.target.nextElementSibling;
    if (content.style.display === 'none') {
        content.style.display = 'block';
        e.target.textContent = '隐藏维基词典内容';
        if (!content.dataset.loaded) {
            const kanji = e.target.dataset.kanji;
            fetchWiktContent(state.wiktFiles[kanji]).then(wiktContent => {
                content.innerHTML = wiktContent;
                content.dataset.loaded = 'true';
            }).catch(error => {
                console.error(`Error loading Wiktionary content for ${kanji}:`, error);
                content.innerHTML = '加载维基词典内容时出错。';
            });
        }
    } else {
        content.style.display = 'none';
        e.target.textContent = '显示维基词典内容';
    }
}

function setupTooltipEventListeners(instance) {
    const toggleButtons = instance.popper.querySelectorAll('.wikt-toggle');
    toggleButtons.forEach(button => {
        // 移除可能存在的旧事件监听器
        button.removeEventListener('click', handleWiktButtonClick);
        // 添加新的事件监听器
        button.addEventListener('click', handleWiktButtonClick);
    });

    instance.popper.addEventListener('mouseenter', () => {
        clearTimeout(state.mouseLeaveTimer);
    });

    instance.popper.addEventListener('mouseleave', () => {
        if (!state.isWiktButtonClicked) {
            startMouseLeaveTimer(instance);
        }
    });
}

function createTippyInstance(element, kanjiInfo) {
    return tippy(element, {
        content: '加载中...',
        allowHTML: true,
        trigger: 'manual',
        hideOnClick: false,
        interactive: true,
        appendTo: () => document.body,
        onShow(instance) {
            state.activeTooltip = instance;
            // 确保在每次显示时都重新设置事件监听器
            setTimeout(() => setupTooltipEventListeners(instance), 0);
        },
        onHide(instance) {
            if (state.activeTooltip === instance) {
                state.activeTooltip = null;
            }
            if (!state.isWiktButtonClicked) {
                state.isWiktButtonClicked = false;
            }
        },
        async onMount(instance) {
            const fullText = instance.reference.dataset.kanji;
            const validKanji = fullText.split('').filter(char => kanjiInfo.hasOwnProperty(char));
            
            if (validKanji.length === 0) {
                instance.setContent(`没有找到有效的汉字信息`);
                return;
            }

            const content = await createTooltipContent(validKanji, kanjiInfo);
            instance.setContent(content);

            const tooltipWidth = calculateTooltipWidth(content);
            instance.setProps({ maxWidth: `${tooltipWidth}px` });

            setTimeout(() => setupTooltipEventListeners(instance), 0);
        },
        popperOptions: {
            modifiers: [
                {
                    name: 'preventOverflow',
                    options: { boundary: document.body },
                },
                {
                    name: 'flip',
                    options: { fallbackPlacements: ['top', 'bottom', 'right', 'left'] },
                },
            ],
        },
    });
}

function handleKanjiMouseEnter(element, tippyInstance, kanjiInfo) {
    clearTimeout(state.mouseLeaveTimer);
    
    if (state.isWiktButtonClicked && state.activeTooltip) {
        return;
    }

    if (state.activeTooltip && state.activeTooltip !== tippyInstance) {
        state.activeTooltip.hide();
    }

    if (!tippyInstance) {
        tippyInstance = createTippyInstance(element, kanjiInfo);
    }
    tippyInstance.show();
    return tippyInstance;
}

function handleKanjiMouseLeave(tippyInstance) {
    if (tippyInstance && !state.isWiktButtonClicked) {
        startMouseLeaveTimer(tippyInstance);
    }
}

function startMouseLeaveTimer(instance) {
    clearTimeout(state.mouseLeaveTimer);
    state.mouseLeaveTimer = setTimeout(() => {
        if (instance === state.activeTooltip && !state.isWiktButtonClicked) {
            instance.hide();
        }
    }, config.mouseLeaveDelay);
}

function handleGlobalClick(event) {
    if (state.activeTooltip && 
        !state.activeTooltip.popper.contains(event.target) && 
        !event.target.classList.contains('kanji')) {
        state.activeTooltip.hide();
        state.isWiktButtonClicked = false;
    }
}

export async function initializeTippy(kanjiInfo) {
    console.time('initializeTippy');
    console.log("Initializing Tippy with kanjiInfo:", Object.keys(kanjiInfo).length);
    await loadWiktFiles();
    if (typeof tippy === 'function') {
        const kanjiElements = document.querySelectorAll('.kanji');
        kanjiElements.forEach(element => {
            let tippyInstance = null;
            element.addEventListener('mouseenter', () => {
                tippyInstance = handleKanjiMouseEnter(element, tippyInstance, kanjiInfo);
            });
            element.addEventListener('mouseleave', () => handleKanjiMouseLeave(tippyInstance));
        });

        document.addEventListener('click', handleGlobalClick);
        console.log("Tippy initialized for kanji elements");
    } else {
        console.error('Tippy.js is not loaded correctly');
    }
    console.timeEnd('initializeTippy');
}