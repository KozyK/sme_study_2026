import urllib.request
from bs4 import BeautifulSoup
import os

url = "https://ai-2ji-shiken.naritai.app/jirei4/d2ji2020"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    code_blocks = soup.find_all('code')
    prompt_text = ""
    for c in code_blocks:
        text = c.get_text()
        if 'AI への指示' in text or '採点官' in text:
            prompt_text = text
            break
            
    if prompt_text:
        target_file = "/Users/kitano52/workspace/sme_study_2026/sessions/2020_jirei4/02_criteria.md"
        
        content = f"""# 令和2年度（2020年度）事例Ⅳ 採点基準（プロンプト）

※AI採点サイト（{url}）から自動取得しました。

```
{prompt_text}
```
"""
        with open(target_file, "w") as f:
            f.write(content)
        print(f"Successfully saved to {target_file}")
    else:
        print("Prompt not found in the page.")
except Exception as e:
    print(f"Error: {e}")
