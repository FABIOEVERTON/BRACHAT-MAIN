import re
import os

pages = [
    "site_oficial/index.html",
    "site_oficial/aigovernance/index.html",
    "site_oficial/publicsector/index.html",
    "site_oficial/rigtech/index.html",
    "site_oficial/academy/index.html"
]

for page in pages:
    if os.path.exists(page):
        with open(page, "r", encoding="utf-8") as f:
            html = f.read()
        
        # Replace 40vh with 12vh
        html = re.sub(
            r'scroll-margin-top:\s*40vh',
            r'scroll-margin-top: 12vh',
            html
        )
        # Also catch the one in the premium override style block
        html = re.sub(
            r'scroll-margin-top:\s*40vh\s*!important',
            r'scroll-margin-top: 12vh !important',
            html
        )
        
        with open(page, "w", encoding="utf-8") as f:
            f.write(html)
            
print("Scroll fixed across all pages!")
