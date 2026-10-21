import sys;sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8')
a=s.index('<div class="arena-wrap"');b=s.index('<div class="bottom">',a);print(s[a:b+180])
