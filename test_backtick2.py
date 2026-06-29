import sys
sys.stdout.reconfigure(encoding='utf-8')
from blog.content.markdown import render_markdown

# Test 1: Normal code block (no escaping needed)
raw1 = r'''---
title: Test
---

```python
print("hello")
```
'''

# Test 2: Escaped backticks (backslash consumed, backticks remain inline)
raw2 = r'''---
title: Test
---

\`\`\`python
print("hello")
\`\`\`
'''

# Test 3: Double-escaped (backslash preserved)
raw3 = r'''---
title: Test
---

\`\`\`python
print("hello")
\`\`\`
'''

for name, raw in [("Normal", raw1), ("Escaped", raw2), ("Double-escaped", raw3)]:
    post = render_markdown('test', raw, 'post')
    print(f"=== {name} ===")
    print(post.html[:300])
    print()
