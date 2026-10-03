with open('api/index.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("    'en': {", "    'en': {\n        'view_all': 'View All',")
content = content.replace("    'ko': {", "    'ko': {\n        'view_all': '모두 보기',")
content = content.replace("    'fr': {", "    'fr': {\n        'view_all': 'Voir tout',")

with open('api/index.py', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
