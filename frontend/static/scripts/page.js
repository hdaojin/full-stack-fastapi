document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/v1/pages/about')
        .then(response => response.json())
        .then(date => {
            const container = document.getElementById('markdown-container');
            container.innerHTML = date.html;
        })
        .catch(error => {
            console.error('Error loading note content:', error);
            document.getElementById('markdown-container').innerHTML = 'Faild to load note content';
        });
});