document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.querySelector('.sidebar');
    const toggleBtn = document.querySelector('.toggle-btn');

    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('expanded');
    });

    const filterDropdown = document.getElementById("filter");

    if (filterDropdown) {
        filterDropdown.addEventListener("change", () => {
            const selected = filterDropdown.value;
            const newUrl = new URL(window.location.href);
            newUrl.searchParams.set("filter", selected);
            window.location.href = newUrl.toString();
        });
    }
});