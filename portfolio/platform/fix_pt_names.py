import re

with open("site_oficial/index.html", "r", encoding="utf-8") as f:
    html = f.read()

def replace_dict_val(lang, key, new_val):
    global html
    pattern = r'(' + lang + r':\s*\{.*?)(\'' + key + r'\':\s*\'.*?\')(.*?\})'
    replacement = r"\1'" + key + "':'" + new_val + r"'\3"
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)

# Fix PT translations names
replace_dict_val('pt', 'ramo1-name', '<span class=\"bt-color\">BT</span> Gov AI')
replace_dict_val('pt', 'ramo2-name', '<span class=\"bt-color\">BT</span> Muni')
replace_dict_val('pt', 'ramo3-name', '<span class=\"bt-color\">BT</span> Rig')

with open("site_oficial/index.html", "w", encoding="utf-8") as f:
    f.write(html)
