import { processKanjiCell, processReadingCell } from './kanjiProcessor.js';
import { setupEventListeners } from './eventHandlers.js';
import { fetchMarkdown, fetchKanjiInfo } from './dataFetcher.js';
import { initializeTippy } from './tippyInitializer.js';
import { handleError } from './utils.js';

export function renderTable(html, tableContainer) {
    tableContainer.innerHTML = html;
    setTimeout(() => processTable(tableContainer), 100);
}

export function processTable(tableContainer, kanjiInfo) {
    console.time('processTable');
    const table = tableContainer.querySelector('table');
    if (table) {
        const headers = table.querySelectorAll('th');
        const headerTexts = Array.from(headers).map(header => header.textContent.trim());
        const kanjiColumnIndex = headerTexts.indexOf('漢字');
        const indexColumnIndex = headerTexts.indexOf('index');
        processTableRows(table, kanjiColumnIndex, indexColumnIndex, headerTexts, kanjiInfo);
    } else {
        console.error("No table found in the parsed HTML");
    }
    console.timeEnd('processTable');
}

function processTableRows(table, kanjiColumnIndex, indexColumnIndex, headerTexts, kanjiInfo) {
    console.time('processTableRows');
    const rows = table.querySelectorAll('tr');
    setAnchors(rows, indexColumnIndex);
    processRowContents(rows, kanjiColumnIndex, indexColumnIndex, headerTexts, kanjiInfo);
    console.timeEnd('processTableRows');
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
            //console.log(`Set anchor for row ${rowIndex}: anchor-${index}`);
        }
    });
}

function processRowContents(rows, kanjiColumnIndex, indexColumnIndex, headerTexts, kanjiInfo) {
    rows.forEach((row, rowIndex) => {
        if (rowIndex === 0) return; // 跳过表头行
        const cells = row.querySelectorAll('td');
        cells.forEach((cell, cellIndex) => {
            if (cellIndex === indexColumnIndex) {
                processIndexCell(cells[0], cell);
            } else if (cellIndex === kanjiColumnIndex) {
                //console.log("Calling processKanjiCell for:", cell.textContent);
                processKanjiCell(cell, kanjiInfo);
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
        const currentFilename = window.location.hash.slice(1).split('#')[0];
        indexCell.innerHTML = `<a href="#${currentFilename}#${index}" class="index-link">${index}</a>`;
        console.log(`Created link for row: #${currentFilename}#${index}`);
    } else {
        indexCell.innerHTML = index;
    }
}


export async function loadMarkdownTable(filename, anchor, tableContainer, kanjiInfo) {
    console.time('loadMarkdownTable');
    try {
        console.time('fetchData');
        const [markdown, kanjiData] = await Promise.all([
            fetchMarkdown(filename),
            fetchKanjiInfo()
        ]);
        console.timeEnd('fetchData');

        kanjiInfo = kanjiData;
        console.log("Kanji info loaded:", Object.keys(kanjiInfo).length);

        console.time('parseMarkdown');
        const html = marked.parse(markdown);
        console.timeEnd('parseMarkdown');

        console.time('renderTable');
        renderTable(html, tableContainer);
        console.timeEnd('renderTable');

        console.time('processTable');
        await processTable(tableContainer, kanjiInfo);
        console.timeEnd('processTable');

        console.log("Table processing complete, initializing Tippy");
        setTimeout(() => {
            console.time('initializeTippy');
            initializeTippy(kanjiInfo);
            console.timeEnd('initializeTippy');

            if (anchor) {
                console.time('scrollToAnchor');
                const targetElement = document.querySelector(`#anchor-${anchor}`);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
                console.timeEnd('scrollToAnchor');
            }
        }, 100);

        setupEventListeners(tableContainer);
    } catch (error) {
        handleError(error, tableContainer);
    }
    console.timeEnd('loadMarkdownTable');
}