import { generateKanjiContent, mergeKanjiInfo, fetchWiktContent } from './kanjiProcessor.js';
import { CONFIG } from './config.js';

const state = {
    // Object to store Wiktionary file paths for each kanji
    wiktFiles: {},

    // Reference to the currently active tooltip instance
    activeTooltip: null,

    // Flag to track if the Wiktionary content button has been clicked
    isWiktButtonClicked: false,

    // Timer for delayed tooltip hiding on mouse leave
    mouseLeaveTimer: null,

    // To prevent other tooltips from being shown when there is any click happend inside the range of the active tooltip
    blockOtherTooltips: false
};

const config = {
    mouseLeaveDelay: 300,
    minTooltipWidth: 0.1,
    maxTooltipWidth: 0.6
};

async function loadWiktFiles() {
    const response = await fetch(CONFIG.KANJI_WIKT_URL);
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
                const wiktContent = await fetchWiktContent(`${CONFIG.KANJI_WIKT_URL}/${state.wiktFiles[kanji]}`);
                if (wiktContent && wiktContent.trim() !== '') {
                    content += `
                        <div class="wikt-content-wrapper">
                            <button class="wikt-toggle" data-kanji="${kanji}">show wikt</button>
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

    state.blockOtherTooltips = true;
    state.isWiktButtonClicked = true;
    const content = e.target.nextElementSibling;
    if (content.style.display === 'none') {
        content.style.display = 'block';
        e.target.textContent = 'hide wikt';
        if (!content.dataset.loaded) {
            const kanji = e.target.dataset.kanji;
            fetchWiktContent(`${CONFIG.KANJI_WIKT_URL}/${state.wiktFiles[kanji]}`).then(wiktContent => {
                content.innerHTML = wiktContent;
                content.dataset.loaded = 'true';
            }).catch(error => {
                console.error(`Error loading Wiktionary content for ${kanji}:`, error);
                content.innerHTML = 'error when loading wikt';
            });
        }
    } else {
        content.style.display = 'none';
        e.target.textContent = 'show wikt';
        state.isWiktButtonClicked = false;
        //state.isWiktButtonClicked = false;
    }
}

function setupTooltipEventListeners(instance) {
    const toggleButtons = instance.popper.querySelectorAll('.wikt-toggle');
    toggleButtons.forEach(button => {
        // remove old event listener if there is any
        button.removeEventListener('click', handleWiktButtonClick);
        // add new event listener
        button.addEventListener('click', handleWiktButtonClick);
    });

    instance.popper.addEventListener('mouseenter', () => {
        clearTimeout(state.mouseLeaveTimer);
    });

    instance.popper.addEventListener('mouseleave', () => {
        if (!state.blockOtherTooltips) {
            startMouseLeaveTimer(instance);
        }
    });
}

function createTippyInstance(element, kanjiInfo) {
    return tippy(element, {
        content: 'loading...',
        allowHTML: true,
        trigger: 'manual',
        hideOnClick: false,
        interactive: true,
        appendTo: () => document.body,
        onShow(instance) {
            state.activeTooltip = instance;
            // ensure event listeners are set up on every show
            setTimeout(() => setupTooltipEventListeners(instance), 0);
            // 添加 tooltip 内部的点击事件监听器
            instance.popper.addEventListener('click', (e) => {
                e.stopPropagation();
                state.blockOtherTooltips = true;
            });
        },
        onHide(instance) {
            if (state.activeTooltip === instance) {
                state.activeTooltip = null;
            }
            if (!state.isWiktButtonClicked) {
                state.isWiktButtonClicked = false;
            }
            if (!state.blockOtherTooltips) {
                state.blockOtherTooltips = false;
            }
        },
        async onMount(instance) {
            const fullText = instance.reference.dataset.kanji;
            const validKanji = fullText.split('').filter(char => kanjiInfo.hasOwnProperty(char));
            
            if (validKanji.length === 0) {
                instance.setContent(`no valid kanji info`);
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
    
    // 如果其他 tooltip 被屏蔽，则不显示新的 tooltip
    if (state.blockOtherTooltips && state.activeTooltip !== tippyInstance) {
        return tippyInstance;
    }

    if (state.activeTooltip && state.activeTooltip !== tippyInstance) {
        // 重置之前的 tooltip 状态
        const prevWiktButton = state.activeTooltip.popper.querySelector('.wikt-toggle');
        const prevWiktContent = state.activeTooltip.popper.querySelector('.wikt-content');
        if (prevWiktButton && prevWiktContent) {
            prevWiktContent.style.display = 'none';
            prevWiktButton.textContent = 'show wikt';
        }
        state.activeTooltip.hide();
    }

    if (!tippyInstance) {
        tippyInstance = createTippyInstance(element, kanjiInfo);
    }
    tippyInstance.show();
    state.isWiktButtonClicked = false;
    return tippyInstance;
}

function handleKanjiMouseLeave(tippyInstance) {
    if (tippyInstance && !state.blockOtherTooltips) {
        startMouseLeaveTimer(tippyInstance);
    }
}

function startMouseLeaveTimer(instance) {
    clearTimeout(state.mouseLeaveTimer);
    state.mouseLeaveTimer = setTimeout(() => {
        if (instance === state.activeTooltip && !state.blockOtherTooltips) {
            instance.hide();
        }
    }, config.mouseLeaveDelay);
}
function handleGlobalClick(event) {
    if (state.activeTooltip) {
        if (!state.activeTooltip.popper.contains(event.target) && 
            !event.target.classList.contains('kanji')) {
            // 点击在 tooltip 外部
            const wiktButton = state.activeTooltip.popper.querySelector('.wikt-toggle');
            const wiktContent = state.activeTooltip.popper.querySelector('.wikt-content');
            if (wiktButton && wiktContent) {
                wiktContent.style.display = 'none';
                wiktButton.textContent = 'show wikt';
            }
            
            state.isWiktButtonClicked = false;
            state.blockOtherTooltips = false;  // 重置屏蔽标志
            startMouseLeaveTimer(state.activeTooltip);  // 启动 mouseleave 的计时
        } else {
            // 点击在 tooltip 内部或触发 tooltip 的汉字上
            event.stopPropagation();
            event.preventDefault();
            state.blockOtherTooltips = true;
        }
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