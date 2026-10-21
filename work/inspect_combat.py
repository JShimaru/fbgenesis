import sys;sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8')
for q in ['id="combatOverlay"','function handleHost','function resolveCombat','function draw(){','function posFor','document.querySelectorAll(\'[data-action]\')']:
 i=s.find(q);print('\n---'+q+'---\n'+s[i:i+1800])
