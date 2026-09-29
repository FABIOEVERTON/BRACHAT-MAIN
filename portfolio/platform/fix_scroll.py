import re

with open("site_oficial/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Adjust scroll-margin-top so sections stop near the middle of the screen
html = re.sub(
    r'section\[id\],div\[id\]\{scroll-margin-top:calc\(var\(--nav-h\) \+ 32px\);\}',
    r'section[id],div[id]{scroll-margin-top: 25vh;}',
    html
)

with open("site_oficial/index.html", "w", encoding="utf-8") as f:
    f.write(html)
