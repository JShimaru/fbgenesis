import sys;sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8')
checks=['style="display:none"','Move north','Tap the arena or use arrow / WASD keys','3–9 breath','12–18 breath','−5 breath','−10 breath','recover 2 breath','mep.x+dx*steps','state.phase===\'move\'&&state.round!==uiRound']
for q in checks:print(repr(q),q in s)
for q in ["function updateUI(){","function draw(){","function selectDirection("]:
 i=s.find(q);print('\n'+s[i:i+500])
