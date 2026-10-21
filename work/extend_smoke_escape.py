from pathlib import Path
p=Path('work/smoke_solo.js');s=p.read_text()
s=s.replace("acts=['block','attack','special'].map", "acts=['block','attack','special','escape'].map")
s=s.replace("const doc={querySelector(q){", "const distances=['1','2','3'].map(x=>{let e=new E();e.dataset.escapeDistance=x;return e}),escapeDirs=['0,-1','-1,0','0,1','1,0'].map(x=>{let e=new E();e.dataset.escapeDir=x;return e});\nconst doc={querySelector(q){")
s=s.replace("q==='[data-action]'?acts:[]", "q==='[data-action]'?acts:q==='[data-escape-distance]'?distances:q==='[data-escape-dir]'?escapeDirs:[]")
s=s.replace("window.__test={get state(){return state},sendState,checkWinner,restartTrial};", "window.__test={get state(){return state},sendState,checkWinner,restartTrial};")
anchor="if(doc.querySelector('#moveControls').classList.contains('hidden'))throw new Error('Movement controls remained hidden');"
addition="""if(doc.querySelector('#moveControls').classList.contains('hidden'))throw new Error('Movement controls remained hidden');
const test=sandbox.window.__test, human=test.state.players.find(p=>p.id==='local-subject'), bot=test.state.players.find(p=>p.bot);human.x=400;human.y=300;human.breath=100;human.shield=0;bot.x=445;bot.y=300;bot.alive=true;bot.dead=false;bot.breath=100;test.state.phase='combat';test.state.fighters=[human.id,bot.id];test.state.combatTurn=1;test.state.actions={[bot.id]:{type:'block'}};test.state.deadline=Date.now()+6000;test.sendState();acts.find(x=>x.dataset.action==='escape').onclick();if(doc.querySelector('#escapeControls').classList.contains('hidden'))throw new Error('Escape route options did not appear');distances.find(x=>x.dataset.escapeDistance==='3').onclick();escapeDirs.find(x=>x.dataset.escapeDir==='-1,0').onclick();doc.querySelector('#confirmEscape').onclick();if(test.state.phase!=='move')throw new Error('Engaged subjects could not exit combat through the escape action');if(human.breath!==94)throw new Error('Escape did not spend two breath per square');"""
s=s.replace(anchor,addition)
s=s.replace("const test=sandbox.window.__test;test.state.players.forEach", "test.state.players.forEach")
s=s.replace("Solo flow smoke check passed: lobby -> breakout -> move -> extinction -> fresh lobby. Vitals, log, map fade and controls verified.", "Smoke check passed: lobby -> breakout -> movement squares -> combat escape (3 squares, 6 breath) -> extinction fade -> re-initiate.")
p.write_text(s)
