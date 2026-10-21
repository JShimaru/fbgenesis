from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')
old="function log(s){logLines.unshift(s);$('#log').innerHTML=logLines.slice(0,12).map(x=>'<div>'+x+'</div>').join('')}"
new="function log(s){logLines.unshift(s);logLines=logLines.slice(0,12);if(host&&state)state.events=logLines.slice();$('#log').innerHTML=logLines.map(x=>'<div>'+x+'</div>').join('')}"
if old not in s: print('log function not found')
else:s=s.replace(old,new,1)
s=s.replace("function updateUI(){if(!state)return;if(state.phase==='combat'", "function updateUI(){if(!state)return;if(Array.isArray(state.events)){logLines=state.events.slice(0,12);$('#log').innerHTML=logLines.map(x=>'<div>'+x+'</div>').join('')}if(state.phase==='combat'",1)
s=s.replace("checkDeaths();let survivors=state.players.filter(p=>p.alive&&!p.contained);", "checkDeaths();log('Movement cycle '+state.round+' resolved.');let survivors=state.players.filter(p=>p.alive&&!p.contained);",1)
p.write_text(s,encoding='utf-8')
