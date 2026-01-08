document.addEventListener('DOMContentLoaded', () => {
    document
        .getElementById('tutorial-form')
        .addEventListener('submit', async (event) => {
            event.preventDefault();
            generateTutorial();
        });
});

async function generateTutorial() {
    const output = document.getElementById('output');
    const imgElement = document.getElementById('myImage');

    output.textContent = 'Generating an image for you...';

    const response = await fetch('/generate', {
        method: 'POST',
        body: new FormData(document.getElementById('tutorial-form'))
    });

    const imageUrl = await response.text();
    imgElement.src = imageUrl;
}

function copyToClipboard() {
    const img = document.getElementById('myImage');
    navigator.clipboard.writeText(img.src);
    alert('Copied to clipboard');
}