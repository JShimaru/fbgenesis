import sys;sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8')
for q in ['.controls{','id="turnbar"','function updateUI(){','function draw(){','document.addEventListener(\'keydown\'']:
 i=s.find(q);print('\n',q,i, s[i:i+600])
