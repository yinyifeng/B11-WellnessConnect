document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.querySelector('.sidebar');
    const toggleBtn = document.querySelector('.toggle-btn');

    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('expanded');
    });
});

function openModal() {
    document.getElementById("uploadModal").style.display = "block";
}

function closeModal() {
    document.getElementById("uploadModal").style.display = "none";
    document.getElementById("imagePreview").style.display = "none";
    document.getElementById("imagePreview").src = "#";
}

// Image preview
function previewImage(event) {
    const preview = document.getElementById("imagePreview");
    const file = event.target.files[0];

    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = "block";
        };
        reader.readAsDataURL(file);
    } else {
        preview.style.display = "none";
    }
}

window.onclick = function(event) {
    const modal = document.getElementById("uploadModal");
    if (event.target == modal) {
        closeModal();
    }
}

window.onload = function () {
    if (window.hasFlashMessage === 'true') {
        openModal();
    }
};
