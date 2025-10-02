// Chapter-specific JavaScript functionality

// Run tests functionality
async function runTests(chapterPath) {
    const btn = document.getElementById('run-tests-btn');
    const output = document.getElementById('test-output');
    const results = document.getElementById('test-results');
    
    if (!btn || !output || !results) return;
    
    btn.disabled = true;
    btn.textContent = 'Running Tests...';
    output.style.display = 'block';
    results.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div> Running tests...';
    
    try {
        const response = await fetch(`/run-tests/${chapterPath}`);
        const data = await response.json();
        
        if (data.success) {
            results.innerHTML = `<pre class="test-output test-success">${data.stdout}</pre>`;
        } else {
            results.innerHTML = `<pre class="test-output test-failure">${data.stderr || data.stdout}</pre>`;
        }
    } catch (error) {
        results.innerHTML = `<pre class="test-output test-failure">Error: ${error.message}</pre>`;
    } finally {
        btn.disabled = false;
        btn.textContent = 'Run Tests';
    }
}

// Toggle code files display
function toggleCode() {
    const codeFiles = document.getElementById('code-files');
    const fileList = document.getElementById('file-list');
    
    if (!codeFiles || !fileList) return;
    
    if (codeFiles.style.display === 'none' || codeFiles.classList.contains('hidden')) {
        codeFiles.style.display = 'block';
        codeFiles.classList.remove('hidden');
        loadCodeFiles();
    } else {
        codeFiles.style.display = 'none';
        codeFiles.classList.add('hidden');
    }
}

// Load code files for the chapter
async function loadCodeFiles(chapterPath) {
    const fileList = document.getElementById('file-list');
    if (!fileList || !chapterPath) return;
    
    fileList.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div> Loading files...';
    
    try {
        const response = await fetch(`/list-files/${chapterPath}`);
        const data = await response.json();
        
        if (data.files) {
            let html = '<div class="row">';
            for (const file of data.files) {
                if (file.name.endsWith('.py')) {
                    html += `
                        <div class="col-md-6 mb-3">
                            <div class="card">
                                <div class="card-header">
                                    <h6 class="mb-0">${file.name}</h6>
                                </div>
                                <div class="card-body">
                                    <button class="btn btn-sm btn-outline-primary" onclick="loadFile('${file.name}', '${chapterPath}')">View Code</button>
                                </div>
                            </div>
                        </div>
                    `;
                }
            }
            html += '</div>';
            fileList.innerHTML = html;
        } else {
            fileList.innerHTML = '<p class="text-muted">No Python files found</p>';
        }
    } catch (error) {
        fileList.innerHTML = `<p class="text-danger">Error loading files: ${error.message}</p>`;
    }
}

// Load and display a specific file
async function loadFile(filename, chapterPath) {
    try {
        const response = await fetch(`/code/${chapterPath}/${filename}`);
        const data = await response.json();
        
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${filename}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <pre><code class="language-python">${data.content}</code></pre>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        
        modal.addEventListener('hidden.bs.modal', () => {
            document.body.removeChild(modal);
        });
    } catch (error) {
        alert(`Error loading file: ${error.message}`);
    }
}



