const tableContainer = document.getElementById('table-container');
const backToHome = document.getElementById('back-to-home');
const backToPrevious = document.getElementById('back-to-previous');

let previousPosition = 0;

async function loadMarkdownTable() {
    try {
        const markdown = await fetchMarkdown();
        const html = parseMarkdown(markdown);
        renderTable(html);
        setupEventListeners();
    } catch (error) {
        handleError(error);
    }
}

async function fetchMarkdown() {
    const timestamp = new Date().getTime();
    const response = await fetch(`ja_onyomi.md?t=${timestamp}`, {
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
                const kanji = instance.reference.textContent;
                instance.setContent(`详细信息: ${kanji}`);
            }
        });
    } else {
        console.error('Tippy.js is not loaded correctly');
    }
}

function setupEventListeners() {
    tableContainer.addEventListener('click', handleTableClick);
    backToHome.addEventListener('click', handleBackToHomeClick);
    backToPrevious.addEventListener('click', handleBackToPreviousClick);
}

function handleTableClick(e) {
    if (e.target.classList.contains('index-link')) {
        e.preventDefault();
        previousPosition = window.pageYOffset;
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
    previousPosition = window.pageYOffset;
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
    previousPosition = window.pageYOffset;
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