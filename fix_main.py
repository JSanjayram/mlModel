import re

# Read the file
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all instances
content = content.replace('use_container_width=True', "width='stretch'")

# Write back
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed all use_container_width instances")