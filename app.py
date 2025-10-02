#!/usr/bin/env python3
"""
Learn Python with Tests - Web Application
A browser-based version of the Python TDD training course.
"""

import os
import subprocess
import markdown
from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path

app = Flask(__name__, static_folder='.', static_url_path='')

# Course structure
COURSE_STRUCTURE = {
    "fundamentals": [
        {"name": "Introduction", "path": "introduction", "description": "TDD basics and setup"},
        {"name": "Hello, world", "path": "hello-world", "description": "Your first Python program with TDD"},
        {"name": "Integers", "path": "integers", "description": "Working with numbers and basic math"},
        {"name": "Iteration", "path": "iteration", "description": "Loops and iteration in Python"},
        {"name": "Arrays", "path": "arrays", "description": "Working with lists and arrays"},
        {"name": "Classes", "path": "classes", "description": "Classes and objects in Python"},
        {"name": "Exceptions", "path": "exceptions", "description": "Exception handling in Python"},
        {"name": "Dictionaries", "path": "dictionaries", "description": "Dictionaries in Python"},
        {"name": "Dependency Injection", "path": "dependency-injection", "description": "Dependency injection patterns"}
    ],
    "advanced": [
        {"name": "Functions & Decorators", "path": "functions-decorators", "description": "Function decorators and closures"},
        {"name": "Generators & Iterators", "path": "generators-iterators", "description": "Lazy evaluation and custom iteration"},
        {"name": "Context Managers", "path": "context-managers", "description": "Resource management with `with` statements"},
        {"name": "Property Decorators", "path": "property-decorators", "description": "`@property`, `@setter`, `@deleter`"},
        {"name": "Magic Methods", "path": "magic-methods", "description": "Dunder methods and object behavior"},
        {"name": "Sets & Data Structures", "path": "sets-data-structures", "description": "Advanced data structures and collections"},
        {"name": "Functional Programming", "path": "functional-programming", "description": "Higher-order functions and immutability"},
        {"name": "Async/Await", "path": "async-await", "description": "Asynchronous programming patterns"},
        {"name": "Web Development", "path": "web-development", "description": "Building web applications with Flask/FastAPI"},
        {"name": "Data Processing", "path": "data-processing", "description": "Working with data using Pandas and NumPy"},
        {"name": "System Programming", "path": "system-programming", "description": "File operations and system interfaces"},
        {"name": "Performance Optimization", "path": "performance-optimization", "description": "Profiling and optimization techniques"}
    ]
}

@app.route('/')
def index():
    """Main course page."""
    return render_template('index.html', course_structure=COURSE_STRUCTURE)

@app.route('/chapter/<path:chapter_path>')
def chapter(chapter_path):
    """Display a specific chapter."""
    # First try to load from content directory (new template-based approach)
    content_path = Path('content') / f'{chapter_path}.html'
    
    if content_path.exists():
        # Read HTML content from content directory
        with open(content_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Get chapter info
        chapter_info = None
        for section in COURSE_STRUCTURE.values():
            for chapter in section:
                if chapter['path'] == chapter_path:
                    chapter_info = chapter
                    break
        
        return render_template('chapter.html', 
                             content=html_content, 
                             chapter_path=chapter_path,
                             chapter_info=chapter_info,
                             course_structure=COURSE_STRUCTURE)
    
    # Fallback to old markdown approach
    chapter_dir = Path(chapter_path)
    readme_path = chapter_dir / 'README.md'
    
    if not readme_path.exists():
        return f"Chapter '{chapter_path}' not found", 404
    
    # Read and convert markdown to HTML
    with open(readme_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    html_content = markdown.markdown(markdown_content, extensions=['codehilite', 'fenced_code'])
    
    # Get chapter info
    chapter_info = None
    for section in COURSE_STRUCTURE.values():
        for chapter in section:
            if chapter['path'] == chapter_path:
                chapter_info = chapter
                break
    
    return render_template('chapter.html', 
                         content=html_content, 
                         chapter_path=chapter_path,
                         chapter_info=chapter_info,
                         course_structure=COURSE_STRUCTURE)

@app.route('/run-tests/<path:chapter_path>')
def run_tests(chapter_path):
    """Run tests for a specific chapter."""
    chapter_dir = Path('source') / chapter_path
    
    if not chapter_dir.exists():
        return jsonify({"error": "Chapter not found"}), 404
    
    try:
        # Change to chapter directory and run tests
        result = subprocess.run(
            ['pytest', '-v', '--tb=short'],
            cwd=chapter_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return jsonify({
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Tests timed out"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/code/<path:chapter_path>/<filename>')
def get_code(chapter_path, filename):
    """Get code files for a chapter."""
    chapter_dir = Path('source') / chapter_path
    file_path = chapter_dir / filename
    
    if not file_path.exists():
        return "File not found", 404
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return jsonify({"content": content})

@app.route('/list-files/<path:chapter_path>')
def list_files(chapter_path):
    """List all files in a chapter directory."""
    chapter_dir = Path('source') / chapter_path
    
    if not chapter_dir.exists():
        return jsonify({"error": "Chapter not found"}), 404
    
    files = []
    for file_path in chapter_dir.iterdir():
        if file_path.is_file() and file_path.suffix in ['.py', '.md']:
            files.append({
                "name": file_path.name,
                "size": file_path.stat().st_size,
                "modified": file_path.stat().st_mtime
            })
    
    return jsonify({"files": files})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

