document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/v1/pages/about')
        .then(response => response.json())
        .then(date => {
            const title = document.getElementsByTagName('title')[0];
            const toc = document.getElementById('toc');
            const container = document.getElementById('markdown-container');
            title.innerHTML = date.title;
            generateTOC(date.toc);
            container.innerHTML = date.html;
        })
        .catch(error => {
            console.error('Error loading content:', error);
            document.getElementById('markdown-container').innerHTML = 'Faild to load content';
        });
});


// Generate Table of Contents function
function generateTOC(tocData) {
    const tocContainer = document.getElementById('toc');
    let currentLevel = 0;
    let stack = [tocContainer];

    tocData.forEach(item => {
        const level = parseInt(item.level[1]);
        const text = item.text;

        const li = document.createElement('li');
        li.textContent = text;

        if (level > currentLevel) {
            const ul = document.createElement('ul');
            stack[stack.length - 1].appendChild(ul);
            ul.appendChild(li);
            stack.push(ul);
        } else {
            while (level < currentLevel) {
                stack.pop();
                currentLevel--;
            }
            stack[stack.length - 1].appendChild(li);
        }
        currentLevel = level;
    });
}