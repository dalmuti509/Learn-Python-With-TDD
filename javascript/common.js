// Common JavaScript functions for Learn Python with Tests

function copyCode(button) {
    const codeBlock = button.parentElement.nextElementSibling;
    const code = codeBlock.textContent;
    
    navigator.clipboard.writeText(code).then(() => {
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        button.classList.add('copied');
        
        setTimeout(() => {
            button.textContent = originalText;
            button.classList.remove('copied');
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy: ', err);
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = code;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        button.classList.add('copied');
        
        setTimeout(() => {
            button.textContent = originalText;
            button.classList.remove('copied');
        }, 2000);
    });
}

// Highlight current page in sidebar
function highlightCurrentPage() {
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.sidebar a[href*="/chapter/"]');
    
    sidebarLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('fw-bold');
            link.style.color = '#0d6efd';
        }
    });
}

// Toggle Green Phase solution visibility
function toggleGreenPhase(button) {
    const solution = button.nextElementSibling;
    const isHidden = solution.style.display === 'none';
    
    if (isHidden) {
        solution.style.display = 'block';
        button.textContent = 'Hide Green Phase Solution';
        button.classList.remove('btn-outline-primary');
        button.classList.add('btn-outline-secondary');
    } else {
        solution.style.display = 'none';
        button.textContent = 'Show Green Phase Solution';
        button.classList.remove('btn-outline-secondary');
        button.classList.add('btn-outline-primary');
    }
}

// Initialize syntax highlighting when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Highlight current page in sidebar
    highlightCurrentPage();
    
    // Prism.js will auto-highlight code blocks
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
    }
});
