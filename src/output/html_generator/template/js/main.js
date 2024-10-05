import { setupEventListeners, handlePopState } from './eventHandlers.js';
import { loadMarkdownTable } from './tableProcessor.js';
import { loadFileList } from './fileList.js';

const tableContainer = document.getElementById('table-container');
let kanjiInfo = null;


function handleHashChange() {
    console.time('handleHashChange');
    const hash = window.location.hash.slice(1);
    if (hash) {
        const [filename, anchor] = hash.split('#');
        loadMarkdownTable(filename, anchor, tableContainer, kanjiInfo);
    } else {
        loadFileList(tableContainer);
    }
    console.timeEnd('handleHashChange');
}

window.addEventListener('hashchange', handleHashChange);
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners(tableContainer);  // 添加这行
    if (window.location.hash) {
        handleHashChange();
    } else {
        loadFileList(tableContainer);
    }
    
    // 添加这行来处理浏览器的后退/前进操作
    window.addEventListener('popstate', handlePopState);
});

export { kanjiInfo };
