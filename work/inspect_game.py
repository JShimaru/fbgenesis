from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8-sig')
for q in ['soloBtn','addBotBtn','PRACTICE BOT','function makeLobby','state.phase=\'combat\'']:
 i=s.find(q); print('\n',q, i, s[max(0,i-120):i+360])
