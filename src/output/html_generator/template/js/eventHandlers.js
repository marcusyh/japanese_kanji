let previousPosition = 0;

export function setupEventListeners(tableContainer) {
    document.getElementById('back-to-home').addEventListener('click', handleBackToHomeClick);
    document.getElementById('back-to-top').addEventListener('click', handleBackToTopClick);
    document.getElementById('back-to-previous').addEventListener('click', handleBackToPreviousClick);
    tableContainer.addEventListener('click', handleTableClick);
}

function handleTableClick(e) {
    if (e.target.classList.contains('index-link')) {
        e.preventDefault();
        previousPosition = window.scrollY;
        const href = e.target.getAttribute('href');
        window.location.hash = href.slice(1); // 这会触发 hashchange 事件
    }
}

function handleBackToHomeClick(e) {
    e.preventDefault();
    window.location.hash = ''; // 清除 hash
    window.dispatchEvent(new HashChangeEvent('hashchange')); // 手动触发 hashchange 事件
}

function handleBackToTopClick(e) {
    e.preventDefault();
    previousPosition = window.scrollY;
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

function handleBackToPreviousClick(e) {
    e.preventDefault();
    window.scrollTo({
        top: previousPosition,
        behavior: 'smooth'
    });
}
