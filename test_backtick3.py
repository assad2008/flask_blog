import sys
sys.stdout.reconfigure(encoding='utf-8')
from blog.content.markdown import render_markdown

# What the user ACTUALLY has in their markdown file:
# literal backslash characters followed by backticks
raw = r'''---
title: Test
---

\`\`\`python
# 代码块会自动语法高亮
def hello():
    print("world")
\`\`\`
'''

print("=== What's in the markdown file (literal chars) ===")
print(repr(raw[raw.index('---')+4:]))
print()
print("=== Current HTML output ===")
post = render_markdown('test', raw, 'post')
print(post.html)
