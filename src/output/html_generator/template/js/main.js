import { fetchMarkdown, fetchKanjiInfo } from './dataFetcher.js';
import { renderTable, processTable } from './tableProcessor.js';
import { initializeTippy } from './tippyInitializer.js';
import { setupEventListeners } from './eventHandlers.js';

const tableContainer = document.getElementById('table-container');
let kanjiInfo = null;

async function loadMarkdownTable() {
    try {
        const [markdown, kanjiData] = await Promise.all([
            fetchMarkdown(),
            fetchKanjiInfo()
        ]);
        kanjiInfo = kanjiData;
        console.log("Kanji info loaded:", Object.keys(kanjiInfo).length); // 添加这行
        const html = marked.parse(markdown);
        renderTable(html, tableContainer);
        await processTable(tableContainer, kanjiInfo);
        console.log("Table processing complete, initializing Tippy");
        setTimeout(() => {
            initializeTippy(kanjiInfo);
        }, 100);
        setupEventListeners(tableContainer);
    } catch (error) {
        handleError(error);
    }
}

function handleError(error) {
    console.error("Error loading or parsing markdown:", error);
    tableContainer.innerHTML = `<p>Error loading content: ${error.message}</p>`;
}

document.addEventListener('DOMContentLoaded', loadMarkdownTable);

export { kanjiInfo };
