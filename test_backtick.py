import sys
sys.stdout.reconfigure(encoding='utf-8')
from blog.content.markdown import render_markdown

# Simulate exactly what the user showed - backslash-escaped backticks
raw = r'''---
title: Test
summary: Test
date: 2024-01-01
---

\`\`\`python
# 代码块会自动语法高亮
def hello():
    print("world")
\`\`\`
'''

print("=== Input (raw markdown) ===")
print(raw)
print("=== Output (HTML) ===")
post = render_markdown('test', raw, 'post')
print(post.html)
