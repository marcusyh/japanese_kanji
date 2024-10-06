export function handleError(error, tableContainer) {
    console.error("Error:", error);
    tableContainer.innerHTML = `<p>Error: ${error.message}</p>`;
}

