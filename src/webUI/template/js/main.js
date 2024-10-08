import { setupEventListeners, handlePopState } from './eventHandlers.js';
import { loadMarkdownTable, processTable } from './tableProcessor.js';
import { loadFileList } from './fileList.js';

const tableContainer = document.getElementById('table-container');
let kanjiInfo = null;

async function handleHashChange() {
    console.time('handleHashChange');
    const hash = window.location.hash.slice(1);
    if (hash) {
        const [filename, anchor] = hash.split('#');
        await loadMarkdownTable(filename, anchor, tableContainer, kanjiInfo);
        processTable(tableContainer, kanjiInfo);
    } else {
        loadFileList(tableContainer);
        // 在显示文件列表时隐藏按钮
        document.getElementById('show/hide-hyogai').style.display = 'none';
        document.getElementById('show/hide-old').style.display = 'none';
    }
    console.timeEnd('handleHashChange');
}

window.addEventListener('hashchange', handleHashChange);
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners(tableContainer);
    if (window.location.hash) {
        handleHashChange();
    } else {
        loadFileList(tableContainer);
    }
    
    window.addEventListener('popstate', handlePopState);
});

// ... 其他函数保持不变

export { kanjiInfo };
