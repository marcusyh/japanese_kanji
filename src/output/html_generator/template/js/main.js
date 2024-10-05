import { fetchMarkdown, fetchKanjiInfo } from './dataFetcher.js';
import { renderTable, processTable } from './tableProcessor.js';
import { initializeTippy } from './tippyInitializer.js';
import { setupEventListeners } from './eventHandlers.js';
import { fetchFileList, renderFileList } from './fileList.js';

const tableContainer = document.getElementById('table-container');
let kanjiInfo = null;

async function loadFileList() {
    try {
        const files = await fetchFileList();
        tableContainer.innerHTML = ''; // 清空容器
        renderFileList(files, tableContainer);
        setupFileListEventListeners();
    } catch (error) {
        handleError(error);
    }
}

async function loadMarkdownTable(filename, anchor) {
    try {
        const [markdown, kanjiData] = await Promise.all([
            fetchMarkdown(filename),
            fetchKanjiInfo()
        ]);
        kanjiInfo = kanjiData;
        console.log("Kanji info loaded:", Object.keys(kanjiInfo).length);
        const html = marked.parse(markdown);
        renderTable(html, tableContainer);
        await processTable(tableContainer, kanjiInfo);
        console.log("Table processing complete, initializing Tippy");
        setTimeout(() => {
            initializeTippy(kanjiInfo);
            if (anchor) {
                const targetElement = document.querySelector(`#anchor-${anchor}`);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            }
        }, 100);
        setupEventListeners(tableContainer);
    } catch (error) {
        handleError(error);
    }
}

function handleError(error) {
    console.error("Error:", error);
    tableContainer.innerHTML = `<p>Error: ${error.message}</p>`;
}

function setupFileListEventListeners() {
    tableContainer.addEventListener('click', (e) => {
        if (e.target.tagName === 'A' && !e.target.classList.contains('index-link')) {
            e.preventDefault();
            const filename = e.target.getAttribute('href').slice(1);
            window.location.hash = filename; // 这会触发 hashchange 事件
        }
    });
}

function handleHashChange() {
    const hash = window.location.hash.slice(1);
    if (hash) {
        const [filename, anchor] = hash.split('#');
        loadMarkdownTable(filename, anchor);
    } else {
        loadFileList();
    }
}

window.addEventListener('hashchange', handleHashChange);
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners(tableContainer);  // 添加这行
    if (window.location.hash) {
        handleHashChange();
    } else {
        loadFileList();
    }
});

export { kanjiInfo };
