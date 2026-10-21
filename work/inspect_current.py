import sys;sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8')
for q in ['<div class="arena-wrap">','function makeLobby','function addBots','function initSolo','function startGame','function updateUI','function draw(){','beginProtocol\').onclick']:
 i=s.find(q);print('\n--- '+q+' @ '+str(i)+' ---\n'+s[i:i+1700])
