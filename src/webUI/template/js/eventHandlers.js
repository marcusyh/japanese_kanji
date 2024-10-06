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
        const [filename, anchor] = href.slice(1).split('#');
        
        // 强制触发滚动，即使哈希值没有改变
        scrollToAnchor(anchor);
        
        // 更新 URL，但不触发页面重载
        history.pushState(null, '', href);
    }
}

function scrollToAnchor(anchor) {
    const targetElement = document.querySelector(`#anchor-${anchor}`);
    if (targetElement) {
        targetElement.scrollIntoView({
            behavior: 'smooth'
        });
    }
}

function handleBackToHomeClick(e) {
    e.preventDefault();
    window.location.hash = '';
}

function handleBackToTopClick(e) {
    e.preventDefault();
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

// 添加这个函数来处理浏览器的后退/前进操作
export function handlePopState() {
    const hash = window.location.hash;
    if (hash) {
        const anchor = hash.split('#')[1];
        scrollToAnchor(anchor);
    } else {
        window.scrollTo(0, 0);
    }
}
