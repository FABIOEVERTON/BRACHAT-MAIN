import re
from bs4 import BeautifulSoup

with open('/Users/mac/.gemini/antigravity/brain/c8399ef0-2597-4683-907c-c8c976ffaead/.system_generated/steps/499/content.md', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Get all text blocks
texts = []
for p in soup.find_all(['h1', 'h2', 'h3', 'p', 'span']):
    text = p.get_text(strip=True)
    if len(text) > 20 and text not in texts:
        texts.append(text)

print("--- INSIDEC WEBSITE CONTENT ---")
for t in texts:
    print(t)

