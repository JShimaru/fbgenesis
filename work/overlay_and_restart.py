from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')
# Move the turn and movement controls into the map viewport, so they overlay the arena.
s=s.replace('</div><div class="turnbar hidden" id="turnbar">','<div class="turnbar hidden" id="turnbar">',1)
s=s.replace('</div><div class="bottom"><span>YOUR MOVE LOCKS WHEN THE TIMER ENDS</span>', '</div></div><div class="bottom"><span>YOUR MOVE LOCKS WHEN THE TIMER ENDS</span>',1)
s=s.replace('<div class="arena-wrap"><canvas', '<div class="arena-wrap" id="arenaWrap"><canvas',1)
# Terminal screen for extinction
needle='<div class="overlay hidden" id="winOverlay"><div class="modal" style="text-align:center"><div class="eyebrow">TRIAL COMPLETE</div><h2>VICTORY</h2><p>One subject remains. Take your Victory Screenshot.</p><button class="primary" id="continueBtn">CONTINUE</button></div></div>'
replacement=needle+'<div class="overlay hidden" id="extinctionOverlay"><div class="modal" style="text-align:center"><div class="eyebrow">TRIAL ARCHIVED</div><h2>NO SUBJECTS REMAIN</h2><p id="extinctionHelp">The trial is complete.</p><button class="primary" id="reinitiateBtn">RE-INITIATE PROTOCOL</button></div></div>'
if needle not in s: print('victory overlay markup not found')
else: s=s.replace(needle,replacement,1)
# Vitals and terminal state, hazards off at the end
s=s.replace("$('#alarm').classList.toggle('on',state.started);", "$('#alarm').classList.toggle('on',state.started&&state.phase!=='ended');")
old="$('#winOverlay').classList.toggle('hidden',state.phase!=='ended'||!state.players.some(x=>x.id===me?.id&&x.alive));$('#combatTimer')"
new="const survivors=state.players.filter(p=>p.alive);$('#winOverlay').classList.toggle('hidden',state.phase!=='ended'||survivors.length!==1||!survivors.some(x=>x.id===me?.id));$('#extinctionOverlay').classList.toggle('hidden',state.phase!=='ended'||survivors.length!==0);$('#arenaWrap').classList.toggle('extinct',state.phase==='ended'&&survivors.length===0);$('#extinctionHelp').textContent=host?'All subjects were terminated. Authorize a fresh trial when ready.':'All subjects were terminated. Awaiting the host to authorize a fresh trial.';$('#reinitiateBtn').classList.toggle('hidden',!host);$('#combatTimer')"
if old not in s: print('win overlay UI fragment not found')
else: s=s.replace(old,new,1)
# Restart all connected human and bot subjects in the same room
insert="""function restartTrial(){if(!host||!state||state.phase!=='ended')return;const old=state.players;state={players:old.map((p,i)=>{const q=posFor(i,old.length);return{id:p.id,name:p.name,x:q.x,y:q.y,breath:100,alive:true,contained:true,dead:false,shield:0,...(p.bot?{bot:true}:{})}}),started:false,phase:'lobby',round:0,deadline:0,fighters:[],moves:{},directions:{},actions:{},purgeAt:0};breakClicks=0;localPod=0;localPodMax=0;moveChoice='wait';moveDir={x:0,y:-1};uiRound=0;logLines=[];log('Fresh subjects assigned. Awaiting protocol authorization.');$('#blackout').classList.add('hidden');sendState();draw()}"""
s=s.replace("function checkWinner(){",insert+"function checkWinner(){",1)
# Restarts can be requested by a non-host after an ending; host remains authoritative.
s=s.replace("function handleHost(from,m){if(!host)return;if(m.type==='join')", "function handleHost(from,m){if(!host)return;if(m.type==='restart'&&state.phase==='ended'){restartTrial();return}if(m.type==='join')",1)
# Purge can terminate the last subject too.
s=s.replace("if(state.players.filter(p=>p.alive).length>1)beginMove();sendState()}", "checkDeaths();if(!checkWinner())beginMove();sendState()}",1)
# Wire reinitiate and final new-game actions to a fresh lobby; clients ask the host.
s=s.replace("$('#newGame').onclick=()=>location.reload();", "$('#newGame').onclick=()=>{if(host)restartTrial();else sendHost({type:'restart'})};$('#reinitiateBtn').onclick=()=>{if(host)restartTrial();else sendHost({type:'restart'})};")
s=s.replace("if(m.type==='state'){const prior=state?.phase;state=m.state;", "if(m.type==='state'){const prior=state?.phase;state=m.state;if(state.phase==='lobby')$('#blackout').classList.add('hidden');")
# Make the map fade for a total extinction; keep the winner's map intact for the screenshot.
s=s.replace('</style>', '''.arena-wrap{position:relative}.turnbar{position:absolute;z-index:3;left:12px;right:12px;top:12px;margin:0;background:#08121eeF;backdrop-filter:blur(6px)}.moveControls{position:absolute;z-index:3;left:12px;right:12px;bottom:12px;margin:0;grid-template-columns:minmax(0,1fr) 190px;background:#08121eef;backdrop-filter:blur(7px)}.arena{transition:opacity .9s ease,filter .9s ease,transform .9s ease}.arena-wrap.extinct .arena{opacity:.12;filter:grayscale(1) blur(3px);transform:scale(.985)}.arena-wrap.extinct .banner,.arena-wrap.extinct .alarm{opacity:0}.arena-wrap.extinct{background:#03070b}.arena-wrap.extinct .overlay{background:#03070bd9}
+@media(max-width:850px){.moveControls{grid-template-columns:minmax(0,1fr) 145px;gap:8px;padding:9px;max-height:76%;overflow:auto}.moveChoices{grid-template-columns:repeat(2,minmax(0,1fr));gap:5px}.moveChoices .control{min-height:48px;padding:7px;font-size:9px}.moveChoices .control strong{font-size:15px}.destination{border-left:1px solid var(--line);border-top:0;padding:0 0 0 7px}.dirgrid{grid-template-columns:38px 38px 38px;grid-template-rows:34px 34px 34px;gap:2px}.dirgrid button{width:38px;height:34px}.dirgrid button b{font-size:16px;line-height:15px}.destinationHint{font-size:7px}.turnbar{top:8px;left:8px;right:8px;padding:9px 11px}.turncopy>span:last-child{font-size:9px}.turncopy strong{font-size:18px}.turnclock{width:62px}.turnclock>span{font-size:24px}.moveControls{left:8px;right:8px;bottom:8px}}
+@media(max-width:390px){.moveControls{grid-template-columns:minmax(0,1fr) 126px}.dirgrid{grid-template-columns:34px 34px 34px;grid-template-rows:31px 31px 31px}.dirgrid button{width:34px;height:31px}.moveChoices .control{padding:5px;font-size:8px}.moveChoices .control strong{font-size:14px}}
+</style>''',1)
# Remove accidental plus prefixes left by prior CSS insertions.
s=s.replace('\n+@media','\n@media')
p.write_text(s,encoding='utf-8')
