from pathlib import Path
p=Path('outputs/index.html')
s=p.read_text(encoding='utf-8-sig')
repls=[
("$('#startBtn').disabled=!(host&&state.players.length>=2&&!state.started);", "$('#startBtn').disabled=!(host&&state.players.length>=2&&!state.started);$('#addBotBtn').disabled=!(host&&!state.started&&state.players.length<8);"),
("<small>${p.alive?'ACTIVE':p.dead?'TERMINATED':'CONTAINED'}</small></div>`).join('');", "<small>${p.bot?'PRACTICE BOT · ':''}${p.alive?'ACTIVE':p.dead?'TERMINATED':'CONTAINED'}</small></div>`).join('');"),
("log('Protocol initiated. Subjects are in containment.');sendState()}", "log('Protocol initiated. Subjects are in containment.');sendState();state.players.filter(p=>p.bot).forEach((p,i)=>setTimeout(()=>handleHost(p.id,{type:'breakout'}),600+i*550+Math.random()*900))}"),
("state.deadline=Date.now()+5000;sendState();setTimeout(resolveMoves,5000)", "state.deadline=Date.now()+5000;state.players.filter(p=>p.bot&&p.alive&&!p.contained).forEach(p=>{state.moves[p.id]=Math.random()<.18?'wait':String(1+Math.floor(Math.random()*3));state.directions[p.id]=direction(p)});sendState();setTimeout(resolveMoves,5000)"),
("state.deadline=Date.now()+3000;log('<b>ENGAGEMENT</b> locked · simultaneous action window.');sendState();", "state.deadline=Date.now()+3000;state.fighters.filter(id=>state.players.find(p=>p.id===id)?.bot).forEach(id=>state.actions[id]=['block','attack','attack','special'][Math.floor(Math.random()*4)]);log('<b>ENGAGEMENT</b> locked · simultaneous action window.');sendState();"),
("$('#createBtn').onclick=()=>{let code=", "function makeLobby(name,code){room=code;host=true;me={id:'local-subject',name};const q=posFor(0,2);state={players:[{id:me.id,name,x:q.x,y:q.y,breath:100,alive:true,contained:true,dead:false,shield:0}],started:false,phase:'lobby',round:0,deadline:0,fighters:[],moves:{},directions:{},actions:{},purgeAt:0};$('#roomCode').textContent=room;$('#startOverlay').classList.add('hidden');sendState()}function addBots(amount){if(!host||!state||state.started)return;for(let j=0;j<amount&&state.players.length<8;j++){let i=state.players.length,q=posFor(i,i+1),num=state.players.filter(p=>p.bot).length+1;state.players.push({id:'practice-bot-'+num,name:['SUBJECT ECHO','SUBJECT NULL','SUBJECT VEGA','SUBJECT KITE','SUBJECT MOTH','SUBJECT ZERO','SUBJECT VANTA'][num-1]||('BOT '+num),x:q.x,y:q.y,breath:100,alive:true,contained:true,dead:false,shield:0,bot:true});state.players.forEach((p,k)=>{let spot=posFor(k,state.players.length);p.x=spot.x;p.y=spot.y})}log('Practice bots added. Bots are local AI opponents for practice.');sendState()}function initSolo(){makeLobby($('#nameInput').value.trim()||'SUBJECT 01','SOLO');addBots(3);log('Solo practice ready. Break containment to begin.');startGame()}$('#soloBtn').onclick=initSolo;$('#addBotBtn').onclick=()=>addBots(1);$('#createBtn').onclick=()=>{let code=")]
for a,b in repls:
 if a not in s: print('MISSING',a[:90])
 else: s=s.replace(a,b,1)
p.write_text(s,encoding='utf-8')

