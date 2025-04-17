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
    const uploadModal = document.getElementById("uploadModal");
    const proofModal = document.getElementById("proofModal");

    if (event.target === uploadModal) {
        closeModal();
    } else if (event.target === proofModal) {
        closeProofModal();
    }
};


window.onload = function () {
    if (window.hasFlashMessage === 'true') {
        openModal();
    }
};

function openProofModal(imageUrl) {
    const modal = document.getElementById('proofModal');
    const img = document.getElementById('proofImagePreview');
    img.src = imageUrl;
    modal.style.display = 'block';
}

function closeProofModal() {
    const modal = document.getElementById('proofModal');
    modal.style.display = 'none';
    document.getElementById('proofImagePreview').src = '#';
}

function toggleLogSection(rowClass, button) {
    const rows = document.querySelectorAll(`.${rowClass}`);
    const isExpanding = button.textContent === "Show All";

    rows.forEach((row, index) => {
        if (index > 0) {
            row.style.display = isExpanding ? 'table-row' : 'none';
        }
    });

    button.textContent = isExpanding ? "Hide" : "Show All";
}


