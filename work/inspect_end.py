import sys;sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8')
for q in ['function restartTrial','function checkWinner','function purge','extinctionOverlay','function log(']:
 i=s.find(q); print('\n---',q,'---\n',s[i:i+1000])
