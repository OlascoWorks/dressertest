const menus = document.querySelectorAll('.nav-link');
menus.forEach((menu) => {
    menu.addEventListener('click', (e) => {
        menus.forEach((menu) => {
            menu.classList.remove('active');
        })

        menu.classList.add('active');
    });
});

// Set the active class based on the current URL
const currentURL = window.location.href;
menus.forEach((menu) => {
    menu.classList.remove('active');
    if (menu.href === currentURL) {
        menu.classList.add('active');
    }
});

// Get the drop zone element
const dropzone = document.querySelector('.dropzone');

// Add event listeners for drag events
dropzone.addEventListener('dragenter', handleDragEnter, false);
dropzone.addEventListener('dragover', handleDragOver, false);
dropzone.addEventListener('dragleave', handleDragLeave, false);
dropzone.addEventListener('drop', handleDrop, false);

function handleDragEnter(e) {
// Highlight the drop zone when a file is dragged over it
dropzone.classList.add('highlight');
}

function handleDragOver(e) {
// Prevent the default drag behavior
e.preventDefault();
}

function handleDragLeave(e) {
// Unhighlight the drop zone when a file is dragged away from it
dropzone.classList.remove('highlight');
}

function handleDrop(e) {
// Prevent the default drop behavior
e.preventDefault();

// Get the file that was dropped
const file = e.dataTransfer.files[0];

// Update the file input element with the dropped file
const fileInput = document.getElementById('image');
fileInput.files = e.dataTransfer.files;

// Update the drop zone text to show the file name
dropzone.innerHTML = file.name;

// Submit the form via AJAX
if (dropzone.id === 'img') {
    const formData = new FormData(document.getElementById('cloth-form'));
} else if (dropzone.id === 'p-img') {
    const formData = new FormData(document.getElementById('signup-form'));
};
const xhr = new XMLHttpRequest();
xhr.open('POST', '/new_cloth');
xhr.setRequestHeader('X-CSRFToken', formData.get('csrf_token'));
xhr.send(formData);
}