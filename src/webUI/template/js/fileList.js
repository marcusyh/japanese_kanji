import { handleError } from './utils.js';
import { CONFIG } from './config.js';

async function fetchFileList() {
    const response = await fetch(CONFIG.FILE_LIST_ENDPOINT);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

function renderFileList(files, container) {
    const ul = document.createElement('ul');
    files.forEach(file => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = `#${file}`;
        a.textContent = file.replace('.md', '');
        li.appendChild(a);
        ul.appendChild(li);
    });
    container.appendChild(ul);
}


export async function loadFileList(tableContainer) {
    try {
        const files = await fetchFileList();
        tableContainer.innerHTML = ''; // 清空容器
        renderFileList(files, tableContainer);
        setupFileListEventListeners(tableContainer);
    } catch (error) {
        handleError(error, tableContainer);
    }
}

function setupFileListEventListeners(tableContainer) {
    tableContainer.addEventListener('click', (e) => {
        if (e.target.tagName === 'A' && !e.target.classList.contains('index-link')) {
            e.preventDefault();
            const filename = e.target.getAttribute('href').slice(1);
            window.location.hash = filename; // 这会触发 hashchange 事件
        }
    });
}

