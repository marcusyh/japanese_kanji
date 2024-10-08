import { CONFIG } from './config.js';

export async function fetchMarkdown(filename) {
    const cleanFilename = filename.split('#')[0];
    const timestamp = new Date().getTime();
    const response = await fetch(`${CONFIG.PRON_LIST_URL}/${cleanFilename}?t=${timestamp}`, {
        headers: {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.text();
}

export async function fetchKanjiInfo() {
    const timestamp = new Date().getTime();
    const response = await fetch(`${CONFIG.WORDS_LIST_URL}?t=${timestamp}`, {
        headers: {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}
