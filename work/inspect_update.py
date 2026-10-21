import sys;sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8')
i=s.index("$('#phase').textContent=")
print(s[i:i+1600])
