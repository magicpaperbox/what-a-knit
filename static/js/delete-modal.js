function openDeleteModal() {
    const modalOverlay = document.getElementById('deleteModal');
    if (modalOverlay) modalOverlay.style.display = 'flex';
}

function closeDeleteModal() {
    const modalOverlay = document.getElementById('deleteModal');
    if (modalOverlay) modalOverlay.style.display = 'none';
}

// Close modal if clicking outside the content box
window.addEventListener('click', function (event) {
    const modalOverlay = document.getElementById('deleteModal');
    if (modalOverlay && event.target === modalOverlay) {
        closeDeleteModal();
    }
});