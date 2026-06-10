import re

with open("/Users/mac/brachat-main/Studies/professional_trail/schedule.md", "r") as f:
    text = f.read()

# Split into entries: each data entry starts with a line matching day+date pattern
# Capture multi-line entries where continuation lines are indented
entries = re.split(r'\n(?=\d[\d.]*(?:-[\d.]+)?\t+\d{2}/\d{2})', text)

header_end = 0
data_entries = []
other = []

for i, entry in enumerate(entries):
    first_line = entry.split('\n')[0]
    if re.match(r'\d[\d.]*(?:-[\d.]+)?\t+\d{2}/\d{2}', first_line.lstrip()):
        data_entries.append(entry)
    else:
        other.append(entry)

header = '\n'.join(other) + '\n'

output_lines = [header]
dia = 1
for entry in data_entries:
    lines = entry.split('\n')
    first = lines[0]
    rest = lines[1:]
    
    parts = first.split('\t')
    day_field = parts[0].strip()
    
    # Calculate how many days this entry spans
    span = 1
    if '-' in day_field and day_field.count('-') == 1:
        try:
            s, e = day_field.split('-')
            # Handle decimal ranges like 16.1 (skip them as single entries)
            if '.' not in s and '.' not in e:
                span = int(e) - int(s) + 1
        except:
            pass
    
    parts[0] = f"Dia {dia}"
    if span > 1:
        parts[0] = f"Dia {dia}-{dia + span - 1}"
    
    parts[1] = ''
    first_fixed = '\t'.join(parts)
    
    # Rejoin with continuation lines
    entry_fixed = first_fixed
    if rest:
        entry_fixed += '\n' + '\n'.join(rest)
    
    output_lines.append(entry_fixed)
    dia += span

output = '\n'.join(output_lines)

with open("/Users/mac/brachat-main/Studies/professional_trail/schedule.md", "w") as f:
    f.write(output)

print(f"Done. Header entries: {len(other)-1}, Data entries: {len(data_entries)}, Last Dia: {dia-1}")
