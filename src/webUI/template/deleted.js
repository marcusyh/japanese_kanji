const tableContainer = document.getElementById('table-container');
const backToHome = document.getElementById('back-to-home');
const backToPrevious = document.getElementById('back-to-previous');

let previousPosition = 0;
let kanjiInfo = null;

async function loadMarkdownTable() {
    try {
        const [markdown, kanjiData] = await Promise.all([
            fetchMarkdown(),
            fetchKanjiInfo()
        ]);
        kanjiInfo = kanjiData;
        const html = parseMarkdown(markdown);
        renderTable(html);
        setupEventListeners();
    } catch (error) {
        handleError(error);
    }
}

async function fetchMarkdown() {
    const timestamp = new Date().getTime();
    const response = await fetch(`data/ja_onyomi.md?t=${timestamp}`, {
        headers: {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    const markdown = await response.text();
    console.log("Markdown content:", markdown.substring(0, 200) + "...");
    return markdown;
}

async function fetchKanjiInfo() {
    const response = await fetch('data/words_list.json');
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

function parseMarkdown(markdown) {
    const html = marked.parse(markdown);
    console.log("Parsed HTML:", html.substring(0, 200) + "...");
    return html;
}

function renderTable(html) {
    tableContainer.innerHTML = html;
    setTimeout(processTable, 100);
}

function processTable() {
    const table = tableContainer.querySelector('table');
    if (table) {
        const headers = table.querySelectorAll('th');
        const headerTexts = Array.from(headers).map(header => header.textContent.trim());
        const kanjiColumnIndex = headerTexts.indexOf('漢字');
        const indexColumnIndex = headerTexts.indexOf('index');
        processTableRows(table, kanjiColumnIndex, indexColumnIndex, headerTexts);
        initializeTippy();
    } else {
        console.error("No table found in the parsed HTML");
    }
}

function processTableRows(table, kanjiColumnIndex, indexColumnIndex, headerTexts) {
    const rows = table.querySelectorAll('tr');
    setAnchors(rows, indexColumnIndex);
    processRowContents(rows, kanjiColumnIndex, indexColumnIndex, headerTexts);
}

function setAnchors(rows, indexColumnIndex) {
    rows.forEach((row, rowIndex) => {
        if (rowIndex === 0) return;
        const cells = row.querySelectorAll('td');
        const firstCell = cells[0];
        const indexCell = cells[indexColumnIndex];
        if (firstCell.textContent.trim() === '○') {
            const index = indexCell.textContent.trim();
            row.id = `anchor-${index}`;
            console.log(`Set anchor for row ${rowIndex}: anchor-${index}`);
        }
    });
}

function processRowContents(rows, kanjiColumnIndex, indexColumnIndex, headerTexts) {
    rows.forEach((row, rowIndex) => {
        if (rowIndex === 0) return; // 跳过表头行
        const cells = row.querySelectorAll('td');
        cells.forEach((cell, cellIndex) => {
            if (cellIndex === indexColumnIndex) {
                processIndexCell(cells[0], cell);
            } else if (cellIndex === kanjiColumnIndex) {
                processKanjiCell(cell);
            } else {
                const header = headerTexts[cellIndex];
                if (header && (header.includes('音') || header.includes('慣用音'))) {
                    processReadingCell(cell);
                }
            }
        });
    });
}

function processIndexCell(firstCell, indexCell) {
    const index = indexCell.textContent.trim();
    if (firstCell.textContent.trim() !== '○') {
        indexCell.innerHTML = `<a href="#anchor-${index}" class="index-link">${index}</a>`;
        console.log(`Created link for row: #anchor-${index}`);
    } else {
        indexCell.innerHTML = index;
    }
}

function processKanjiCell(kanjiCell) {
    const kanji = kanjiCell.textContent.trim().split('、');
    kanjiCell.innerHTML = kanji.map(k => `<span class="kanji">${k}</span>`).join('、');
    kanjiCell.addEventListener('mousemove', handleKanjiMouseMove);
}

function handleKanjiMouseMove(event) {
    const target = event.target;
    if (target.classList.contains('kanji')) {
        const rect = target.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const charWidth = rect.width / target.textContent.length;
        const charIndex = Math.floor(x / charWidth);
        target.dataset.hoverChar = target.textContent[charIndex];
    }
}

function processReadingCell(cell) {
    const readings = cell.textContent.trim().split('、');
    cell.innerHTML = readings.map(reading => `<span class="reading">${reading}</span>`).join('、');
}

function initializeTippy() {
    if (typeof tippy === 'function') {
        tippy('.kanji', {
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
    } else {
        console.error('Tippy.js is not loaded correctly');
    }
}

function generateKanjiContent(kanji, info) {
    let content = `<div class="kanji-info"><h3>${kanji}</h3>`;
    if (info['音読み'] && Array.isArray(info['音読み'])) {
        content += '<h4>音読み</h4>';
        info['音読み'].forEach(reading => {
            if (reading && typeof reading === 'object') {
                const pron = reading.pron || '不明';
                const type = reading.type || '不明';
                const wordsList = Array.isArray(reading.words_list) ? reading.words_list.join(', ') : '无例词';
                content += `<p><strong>${pron}</strong> (${type}): ${wordsList}</p>`;
            }
        });
    }
    if (info['訓読み'] && Array.isArray(info['訓読み'])) {
        content += '<h4>訓読み</h4>';
        info['訓読み'].forEach(reading => {
            if (reading && typeof reading === 'object') {
                const pron = reading.pron || '不明';
                const wordsList = Array.isArray(reading.words_list) ? reading.words_list.join(', ') : '无例词';
                content += `<p><strong>${pron}</strong>: ${wordsList}</p>`;
            }
        });
    }
    content += '</div>';
    return content;
}

function setKanjiContent(instance, kanji, info) {
    instance.setContent(generateKanjiContent(kanji, info));
}

function setupEventListeners() {
    tableContainer.addEventListener('click', handleTableClick);
    backToHome.addEventListener('click', handleBackToHomeClick);
    backToPrevious.addEventListener('click', handleBackToPreviousClick);
}

function handleTableClick(e) {
    if (e.target.classList.contains('index-link')) {
        e.preventDefault();
        previousPosition = window.scrollY;
        const href = e.target.getAttribute('href');
        const targetElement = document.querySelector(href);
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth'
            });
        }
    }
}

function handleAnchorClick(e) {
    e.preventDefault();
    previousPosition = window.scrollY;
    const href = this.getAttribute('href');
    const targetElement = document.querySelector(href);
    if (targetElement) {
        targetElement.scrollIntoView({
            behavior: 'smooth'
        });
    }
}

function handleBackToHomeClick(e) {
    e.preventDefault();
    previousPosition = window.scrollY;
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

function handleBackToPreviousClick(e) {
    e.preventDefault();
    window.scrollTo({
        top: previousPosition,
        behavior: 'smooth'
    });
}

function handleError(error) {
    console.error("Error loading or parsing markdown:", error);
    tableContainer.innerHTML = `<p>Error loading content: ${error.message}</p>`;
}

document.addEventListener('DOMContentLoaded', loadMarkdownTable);