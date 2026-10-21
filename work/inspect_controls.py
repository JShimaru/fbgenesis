import sys;sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8')
for q in ['<div class="controls" id="moveControls"','function updateUI(){','function draw(){','document.querySelectorAll(\'[data-move]\')','cv.addEventListener']:
 i=s.find(q);print('\n---',q,i,'---\n',s[i:i+1100])
