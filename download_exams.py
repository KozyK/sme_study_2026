import os
import re
import urllib.request
import urllib.error
import time

input_file = '/Users/kitano52/workspace/shikenmondai.html'
output_dir = '/Users/kitano52/workspace/sme_study_2026/past_exams/2nd_stage'
base_url = 'https://www.jf-cmca.jp'

os.makedirs(output_dir, exist_ok=True)

with open(input_file, 'r', encoding='latin-1') as f:
    content = f.read()

# Find all hrefs containing '2ji' or '2JI' ending with pdf
matches = re.findall(r'href="(\.\./\.\./attach/test/shikenmondai/(?:2ji|2JI)[^"]+\.pdf)"', content, re.IGNORECASE)

print(f"Found {len(matches)} files to download.")

for match in matches:
    url_path = match.replace('../../', '/')
    url = base_url + url_path
    
    filename = os.path.basename(match)
    
    # create a subdirectory for the year
    year_match = re.search(r'2ji(\d{4})', match, re.IGNORECASE)
    if year_match:
        year = year_match.group(1)
        year_dir = os.path.join(output_dir, year)
        os.makedirs(year_dir, exist_ok=True)
        filepath = os.path.join(year_dir, filename)
    else:
        filepath = os.path.join(output_dir, filename)
    
    if os.path.exists(filepath):
        print(f"Already exists: {filepath}")
        continue
        
    print(f"Downloading {url} to {filepath}")
    try:
        # Add headers to avoid 403 Forbidden just in case
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        time.sleep(0.5) # Be polite to the server
    except urllib.error.URLError as e:
        print(f"Failed to download {url}: {e}")

print("Download complete.")
