export function processKanjiCell(kanjiCell, kanjiInfo) {
    //console.log("Processing kanji cell:", kanjiCell.textContent);
    const kanji = kanjiCell.textContent.trim().split('、');
    kanjiCell.innerHTML = kanji.map(k => `<span class="kanji" data-kanji="${k}">${k}</span>`).join('、');
    //console.log("Processed kanji cell:", kanjiCell.innerHTML);
    kanjiCell.addEventListener('mousemove', handleKanjiMouseMove);
}

export function processReadingCell(cell) {
    const readings = cell.textContent.trim().split('、');
    cell.innerHTML = readings.map(reading => `<span class="reading">${reading}</span>`).join('、');
}

function handleKanjiMouseMove(event) {
    const target = event.target;
    if (target.classList.contains('kanji')) {
        const rect = target.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const charWidth = rect.width / target.textContent.length;
        const charIndex = Math.floor(x / charWidth);
        target.dataset.hoverChar = target.textContent[charIndex];
    }
}

export function mergeKanjiInfo(kanjiInfoArray) {
    const groups = [];
    const processed = new Set();

    for (let i = 0; i < kanjiInfoArray.length; i++) {
        if (processed.has(i)) continue;

        const currentGroup = { kanji: [kanjiInfoArray[i].kanji], info: kanjiInfoArray[i].info };
        processed.add(i);

        for (let j = i + 1; j < kanjiInfoArray.length; j++) {
            if (processed.has(j)) continue;

            if (JSON.stringify(kanjiInfoArray[i].info) === JSON.stringify(kanjiInfoArray[j].info)) {
                currentGroup.kanji.push(kanjiInfoArray[j].kanji);
                processed.add(j);
            }
        }

        groups.push(currentGroup);
    }

    return groups;
}

export function generateKanjiContent(kanji, info) {
    let content = `<div class="kanji-info"><h3>${kanji}</h3>`;
    if (info['音読み'] && Array.isArray(info['音読み'])) {
        content += '<h4>音読み</h4>';
        info['音読み'].forEach(reading => {
            if (reading && typeof reading === 'object') {
                const pron = reading.pron || '不明';
                const type = reading.type || '不明';
                const wordsList = Array.isArray(reading.words_list) ? reading.words_list.join(', ') : '无例词';
                content += `<p><strong>${pron}</strong> (${type}): ${wordsList}</p>`;
            }
        });
    }
    if (info['訓読み'] && Array.isArray(info['訓読み'])) {
        content += '<h4>訓読み</h4>';
        info['訓読み'].forEach(reading => {
            if (reading && typeof reading === 'object') {
                const pron = reading.pron || '不明';
                content += `<div class="kunyomi-group">`;
                content += `<p class="main-pron"><strong>${pron}</strong></p>`;
                if (reading.words_list && typeof reading.words_list === 'object') {
                    Object.entries(reading.words_list).forEach(([subPron, words]) => {
                        content += `<div class="sub-pron-group">`;
                        const words_str = Array.isArray(words) && words.length > 0 ? words.join('、') : '无例词';
                        content += `<p class="sub-pron">&nbsp;&nbsp;${subPron}：${words_str}</p>`;
                        content += `</div>`;
                    });
                } else {
                    content += `<p class="no-words">无例词</p>`;
                }
                content += `</div>`;
            }
        });
    }
    content += '</div>';
    return content;
}

export async function fetchWiktContent(filePath) {
    const response = await fetch(filePath);
    const html = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    // 这里可以根据维基词典 HTML 的结构来提取所需的内容
    // 这只是一个示例，您可能需要根据实际 HTML 结构进行调整
    const content = doc.querySelector('body').innerHTML;
    return content;
}
