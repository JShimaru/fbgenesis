from pathlib import Path
p=Path('outputs/index.html')
s=p.read_text(encoding='utf-8')
s=s.replace("$('#roomCode').textContent=room;$('#startOverlay').classList.add('hidden');sendState()}function addBots", "$('#roomCode').textContent=room;$('#net').textContent=code==='SOLO'?'LOCAL PRACTICE':'CONNECTING';$('#startOverlay').classList.add('hidden');sendState()}function addBots")
p.write_text(s,encoding='utf-8')
