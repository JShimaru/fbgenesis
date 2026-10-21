from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')
old="window.addEventListener('resize',()=>{if(state?.phase!=='ended')return;const alive=state.players.filter(p=>p.alive),self=state.players.find(p=>p.id===me?.id);if(alive.length===0)positionTrialDebrief('extinct',state.players);else if(alive.length===1)positionTrialDebrief(self?.alive?'winner':'fixed',state.players)});"
new="if(window.addEventListener)window.addEventListener('resize',()=>{if(state?.phase!=='ended')return;const alive=state.players.filter(p=>p.alive),self=state.players.find(p=>p.id===me?.id);if(alive.length===0)positionTrialDebrief('extinct',state.players);else if(alive.length===1)positionTrialDebrief(self?.alive?'winner':'fixed',state.players)});"
assert old in s
p.write_text(s.replace(old,new,1),encoding='utf-8')
print('Made resize listener compatible with embedded runtime.')
