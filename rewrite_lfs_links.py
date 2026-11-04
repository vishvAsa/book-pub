import os
import re
from pathlib import Path

# Get environment variables provided by GitHub Actions
repo = os.getenv('GITHUB_REPOSITORY', 'vishvasa/book-pub')
branch = os.getenv('GITHUB_REF_NAME', 'master')

# Define base URLs
PREVIEW_BASE = f"https://github.com/{repo}/blob/{branch}"
DIRECT_BASE = f"https://media.githubusercontent.com/media/{repo}/{branch}"

# Regex to find: <a href="./filename.pdf">filename.pdf</a>
# Group 1: the filename/path. Group 2: the display text.
LINK_PATTERN = re.compile(r'<a href="\./([^" ]*\.pdf)">([^<]*)</a>')

def process_file(file_path):
  # Calculate the folder path relative to the root
  # e.g., if file is './vedAH/index.html', dir_prefix is 'vedAH/'
  relative_dir = file_path.parent.relative_to('.')
  dir_prefix = "" if str(relative_dir) == "." else f"{relative_dir}/"

  print(f"Processing: {file_path} (Prefix: {dir_prefix})")

  with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

  def replace_link(match):
    file_name = match.group(1)
    display_text = match.group(2)

    preview_url = f"{PREVIEW_BASE}/{dir_prefix}{file_name}"
    download_url = f"{DIRECT_BASE}/{dir_prefix}{file_name}"

    return (f'{display_text}: '
            f'[<a href="{preview_url}">Preview</a>] '
            f'[<a href="{download_url}">Download</a>]')

  new_content = LINK_PATTERN.sub(replace_link, content)

  with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

if __name__ == "__main__":
  # Recursively find all index.html files
  for path in Path('.').rglob('index.html'):
    process_file(path)