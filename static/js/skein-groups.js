const toggleButtons = document.querySelectorAll('.skein-toggle-button');

toggleButtons.forEach((button) => {
    button.addEventListener('click', () => {
        const groupId = button.dataset.group;
        const groupRow = document.querySelector(`.skein-group-row[data-group="${groupId}"]`);
        const childRows = document.querySelectorAll(`.skein-child-row[data-group="${groupId}"]`);
        const icon = button.querySelector('.skein-toggle-icon');

        const isExpanded = groupRow.classList.toggle('is-expanded');

        childRows.forEach((row) => {
            row.classList.toggle('is-expanded');
        });

        if (isExpanded) {
            icon.src = '/static/icons/up-arrow.png';
            icon.alt = 'Collapse';
        } else {
            icon.src = '/static/icons/down-arrow.png';
            icon.alt = 'Expand';
        }

    });
});


