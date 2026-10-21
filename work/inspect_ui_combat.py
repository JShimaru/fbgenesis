import sys;sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8')
for q in ['function updateUI(){','document.querySelectorAll(\'[data-action]\').forEach']:
 i=s.index(q);print('\n'+s[i:i+1400])
