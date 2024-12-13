#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    if sys.version_info < (3, 7):
        print("Python 3.7 or higher is required")
        sys.exit(1)

def install_requirements():
    print("Installing required packages...")
    requirements_path = Path(__file__).parent / "requirements.txt"
    if not requirements_path.exists():
        print("Error: requirements.txt not found")
        sys.exit(1)
    
    result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_path)])
    if result.returncode != 0:
        print("Error installing requirements")
        sys.exit(1)

def create_env_file():
    env_example = Path(__file__).parent / ".env.example"
    env_file = Path(__file__).parent / ".env"
    
    if not env_file.exists():
        print("\nCreating .env file...")
        if env_example.exists():
            env_example.rename(env_file)
        else:
            print("Error: .env.example not found")
            sys.exit(1)
    
    print("\nPlease edit .env file with your configuration:")
    print(f"Path: {env_file.absolute()}")

def main():
    print("Setting up AI Calendar...")
    
    check_python_version()
    install_requirements()
    create_env_file()
    
    print("\nSetup complete! Next steps:")
    print("1. Edit the .env file with your configuration")
    print("2. Run 'python3 install.py' to install the launch agent")

if __name__ == "__main__":
    main() 