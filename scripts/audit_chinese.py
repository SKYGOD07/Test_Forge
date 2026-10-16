import os
import re
from pathlib import Path

CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff]')

IGNORE_DIRS = {
    '.git', '.venv', 'node_modules', 'dist', '__pycache__', '.idea', '.vscode'
}

TEXT_EXTENSIONS = {
    '.py', '.js', '.vue', '.html', '.css', '.json', '.md', '.yml', '.yaml',
    '.toml', '.txt', '.dockerignore', '.gitignore', 'Dockerfile'
}

def scan_repo(root_dir):
    matches = {}
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in TEXT_EXTENSIONS or file in {'Dockerfile', '.env.example'}:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                    file_matches = []
                    for idx, line in enumerate(lines, 1):
                        if CHINESE_PATTERN.search(line):
                            file_matches.append((idx, line.strip()))
                    if file_matches:
                        rel_path = file_path.relative_to(root_dir)
                        matches[str(rel_path)] = file_matches
                except Exception as e:
                    pass
    return matches

if __name__ == '__main__':
    workspace = Path(__file__).resolve().parent.parent
    results = scan_repo(workspace)
    print(f"Found Chinese characters in {len(results)} files:")
    for path, lines in sorted(results.items()):
        print(f"  {path}: {len(lines)} lines")
