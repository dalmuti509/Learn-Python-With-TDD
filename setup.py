#!/usr/bin/env python3
"""
Setup script for Learn Python with Tests
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a command and return the result."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def setup_environment():
    """Set up the development environment."""
    print("Setting up Learn Python with Tests environment...")
    
    # Check if Python is installed
    python_version = run_command("python --version")
    if python_version:
        print(f"Python version: {python_version.strip()}")
    else:
        print("Error: Python is not installed or not in PATH")
        return False
    
    # Check if pip is installed
    pip_version = run_command("pip --version")
    if pip_version:
        print(f"pip version: {pip_version.strip()}")
    else:
        print("Error: pip is not installed or not in PATH")
        return False
    
    # Install requirements
    print("Installing requirements...")
    install_result = run_command("pip install -r requirements.txt")
    if install_result:
        print("Requirements installed successfully!")
    else:
        print("Error installing requirements")
        return False
    
    # Verify pytest installation
    pytest_version = run_command("pytest --version")
    if pytest_version:
        print(f"pytest version: {pytest_version.strip()}")
    else:
        print("Error: pytest installation failed")
        return False
    
    print("\nEnvironment setup complete!")
    print("\nTo get started:")
    print("1. Read the introduction: introduction/README.md")
    print("2. Start with Hello World: hello-world/README.md")
    print("3. Run tests: pytest")
    
    return True

if __name__ == "__main__":
    success = setup_environment()
    if not success:
        sys.exit(1)


