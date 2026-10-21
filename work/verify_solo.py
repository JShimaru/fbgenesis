import sys;sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8')
for q in ['let peer=null','function updateUI(){','function startGame(){','function breakGlass()','class="controls moveControls']:
 i=s.find(q);print('\n',q, s[i:i+300])
