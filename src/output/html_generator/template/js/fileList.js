export async function fetchFileList() {
    const response = await fetch('/file_list');
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

export function renderFileList(files, container) {
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
