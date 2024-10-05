let previousPosition = 0;

export function setupEventListeners(tableContainer) {
    tableContainer.addEventListener('click', handleTableClick);
    document.getElementById('back-to-home').addEventListener('click', handleBackToHomeClick);
    document.getElementById('back-to-previous').addEventListener('click', handleBackToPreviousClick);
}

function handleTableClick(e) {
    if (e.target.classList.contains('index-link')) {
        e.preventDefault();
        previousPosition = window.scrollY;
        const href = e.target.getAttribute('href');
        const targetElement = document.querySelector(href);
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth'
            });
        }
    }
}

function handleBackToHomeClick(e) {
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
