#!/usr/bin/env python3

import sys

def check_import(package_name, import_name=None):
    if import_name is None:
        import_name = package_name
    try:
        __import__(import_name)
        print(f"✓ {package_name} installed successfully")
        return True
    except ImportError:
        print(f"✗ {package_name} NOT installed")
        return False

print("Checking Python environment...")
print(f"Python version: {sys.version}")
print()

print("Checking required packages:")
packages = [
    ("LangChain", "langchain"),
    ("Sentence-Transformers", "sentence_transformers"),
    ("ChromaDB", "chromadb"),
    ("NumPy", "numpy"),
    ("Pandas", "pandas"),
    ("Matplotlib", "matplotlib"),
    ("Plotly", "plotly"),
]

all_installed = True
for name, import_name in packages:
    if not check_import(name, import_name):
        all_installed = False

print()
if all_installed:
    print("All packages installed successfully!")
else:
    print("Some packages are missing. Run: pip install -r requirements.txt")
    sys.exit(1)
