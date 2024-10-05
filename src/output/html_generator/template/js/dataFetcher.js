export async function fetchMarkdown() {
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

export async function fetchKanjiInfo() {
    const response = await fetch('data/words_list.json');
    //console.log(response)
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}
