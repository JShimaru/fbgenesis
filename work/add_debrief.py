from pathlib import Path
p=Path('outputs/index.html')
s=p.read_text(encoding='utf-8')

# Compact debrief takes the upper-right timer position once the trial ends.
needle='</div></div><div class="controls moveControls hidden" id="moveControls"'
replacement='</div></div><section class="trialDebrief hidden" id="trialDebrief" aria-live="polite" aria-label="Trial debrief"><div class="debriefHead"><span class="eyebrow">TRIAL DEBRIEF</span><strong id="debriefResult">TRIAL ARCHIVED</strong></div><div class="debriefSubject" id="debriefSubject">SUBJECT</div><div class="debriefGrid"><span>BREAKOUT</span><b id="debriefBreakout">—</b><span>ROUNDS SURVIVED</span><b id="debriefRounds">—</b><span>STRIKES LANDED</span><b id="debriefHits">—</b><span>SPECIALS · BLOCKS</span><b id="debriefCombat">—</b><span>ESCAPES CLEAR · FAILED</span><b id="debriefEscapes">—</b></div></section><div class="controls moveControls hidden" id="moveControls"'
assert needle in s
s=s.replace(needle,replacement,1)

# Add a small, readable outcome cue for combat resolution effects.
needle="}else if(e.type==='escape'){\n   for(let i=0;i<(e.spots||[]).length;i++)"
replacement="}else if(e.type==='outcome'){\n   const x=e.target.x,y=e.target.y-34-progress*15;cx.globalAlpha=fade;cx.textAlign='center';cx.font='bold 9px IBM Plex Mono';cx.lineWidth=3;cx.strokeStyle='#071019';cx.strokeText(e.text,x,y);cx.fillStyle=e.tone==='good'?'#baffef':e.tone==='bad'?'#ff9ca5':'#eafaff';cx.fillText(e.text,x,y);cx.textAlign='left'\n  }else if(e.type==='escape'){\n   for(let i=0;i<(e.spots||[]).length;i++)"
assert needle in s
s=s.replace(needle,replacement,1)

# Set up per-subject stats when a trial starts.
needle="state.started=true;state.phase='breakout';localPod=30+Math.floor(Math.random()*16);"
replacement="state.started=true;state.phase='breakout';state.breakoutCount=0;state.players.forEach(p=>{p.stats={breakoutOrder:null,regularAttacks:0,specialAttacks:0,hits:0,blocks:0,escapesClear:0,escapesFailed:0,roundsSurvived:0,impactRounds:0}});localPod=30+Math.floor(Math.random()*16);"
assert needle in s
s=s.replace(needle,replacement,1)

# Count natural breakouts in order.
needle="if(m.type==='breakout'){let p=state.players.find(x=>x.id===from);if(!p||!p.contained)return;p.contained=false;"
replacement="if(m.type==='breakout'){let p=state.players.find(x=>x.id===from);if(!p||!p.contained)return;p.stats=p.stats||{};if(!p.stats.breakoutOrder)p.stats.breakoutOrder=++state.breakoutCount;p.contained=false;"
assert needle in s
s=s.replace(needle,replacement,1)
# Forced ejections follow any subjects that broke out naturally.
needle="state.players.filter(p=>p.contained&&p.alive).forEach(p=>{p.contained=false;p.breath-=15;"
replacement="state.players.filter(p=>p.contained&&p.alive).forEach(p=>{p.stats=p.stats||{};if(!p.stats.breakoutOrder)p.stats.breakoutOrder=++state.breakoutCount;p.contained=false;p.breath-=15;"
assert needle in s
s=s.replace(needle,replacement,1)

# Track attacks/actions, actual impact after block/escape/shield, and brief outcome labels.
needle="damage=Object.fromEntries(active.map(p=>[p.id,0])),escapeRoutes={},actionById={},visuals=[],damageSpots={};"
replacement="damage=Object.fromEntries(active.map(p=>[p.id,0])),escapeRoutes={},actionById={},visuals=[],damageSpots={},attackEvents=[],actualDamage=Object.fromEntries(active.map(p=>[p.id,0]));"
assert needle in s
s=s.replace(needle,replacement,1)
needle="actionById[p.id]=a;const targets=nearbyOpponents(p),from={x:p.x,y:p.y};if(a.type==='attack'||a.type==='special'){const attack="
replacement="actionById[p.id]=a;p.stats=p.stats||{};if(a.type==='block')p.stats.blocks=(p.stats.blocks||0)+1;if(a.type==='attack')p.stats.regularAttacks=(p.stats.regularAttacks||0)+1;if(a.type==='special')p.stats.specialAttacks=(p.stats.specialAttacks||0)+1;const targets=nearbyOpponents(p),from={x:p.x,y:p.y};if(a.type==='attack'||a.type==='special'){const attack="
assert needle in s
s=s.replace(needle,replacement,1)
needle="for(const t of hits){damage[t.id]+=dealt;(damageSpots[t.id]||(damageSpots[t.id]={x:t.x,y:t.y}));}visuals.push"
replacement="for(const t of hits){damage[t.id]+=dealt;(damageSpots[t.id]||(damageSpots[t.id]={x:t.x,y:t.y}));attackEvents.push({source:p.id,target:t.id,kind:a.type});}visuals.push"
assert needle in s
s=s.replace(needle,replacement,1)
needle="escapeOutcomes[result.p.id]={success,moved:result.moved};visuals.push({type:'escape',spots,success});log(success?'<b>'+esc(result.p.name)+'</b> escaped the engagement.':'<b>'+esc(result.p.name)+'</b> could not clear the engagement.')"
replacement="escapeOutcomes[result.p.id]={success,moved:result.moved};result.p.stats=result.p.stats||{};const escapeKey=success?'escapesClear':'escapesFailed';result.p.stats[escapeKey]=(result.p.stats[escapeKey]||0)+1;visuals.push({type:'escape',spots,success});visuals.push({type:'outcome',target:{x:result.p.x,y:result.p.y},text:success?'ESCAPE CLEAR':'ESCAPE INTERCEPTED',tone:success?'good':'bad'});log(success?'<b>'+esc(result.p.name)+'</b> escaped cleanly · incoming strikes avoided.':'<b>'+esc(result.p.name)+'</b> was intercepted · impact reduced, not avoided.')"
assert needle in s
s=s.replace(needle,replacement,1)
needle="if(incoming>0){p.breath-=incoming;visuals.push({type:'breath',spots:[damageSpots[p.id]||{x:p.x,y:p.y}],intensity:.13})}if(a.type==='escape')"
replacement="actualDamage[p.id]=incoming;if(incoming>0){p.breath-=incoming;p.stats=p.stats||{};p.stats.impactRounds=(p.stats.impactRounds||0)+1;visuals.push({type:'breath',spots:[damageSpots[p.id]||{x:p.x,y:p.y}],intensity:.13});visuals.push({type:'outcome',target:{x:p.x,y:p.y},text:a.type==='block'?'BLOCK HELD · IMPACT':'IMPACT RECEIVED',tone:'bad'})}else if(a.type==='block'){visuals.push({type:'outcome',target:{x:p.x,y:p.y},text:'BLOCK READY',tone:'good'})}else if(a.type==='escape'&&escapeOutcomes[p.id]?.success){visuals.push({type:'outcome',target:{x:p.x,y:p.y},text:'NO IMPACT',tone:'good'})}if(a.type==='escape')"
assert needle in s
s=s.replace(needle,replacement,1)
needle="state.visualEffects=visuals.map(v=>({...v,at:Date.now(),duration:1050}));checkDeaths();log('Round '+state.round+' resolved · movement and engagements processed together.');"
replacement="for(const event of attackEvents){const target=state.players.find(q=>q.id===event.target),source=state.players.find(q=>q.id===event.source),evaded=escapeOutcomes[event.target]?.success;if(!target||!source)continue;if(!evaded){source.stats=source.stats||{};source.stats.hits=(source.stats.hits||0)+1}const label=evaded?'STRIKE EVADED':event.kind==='special'?'SPECIAL LANDED':'STRIKE LANDED';visuals.push({type:'outcome',target:{x:target.x,y:target.y},text:label,tone:evaded?'good':'neutral'});log(evaded?'<b>'+esc(target.name)+'</b> evaded '+esc(source.name)+'’s '+(event.kind==='special'?'special':'strike')+'.':'<b>'+esc(source.name)+'</b>’s '+(event.kind==='special'?'special':'strike')+' connected with <b>'+esc(target.name)+'</b>.')}state.visualEffects=visuals.map(v=>({...v,at:Date.now(),duration:1250}));checkDeaths();state.players.forEach(p=>{p.stats=p.stats||{};if(p.alive)p.stats.roundsSurvived=state.round});log('Round '+state.round+' resolved · movement and engagements processed together.');"
assert needle in s
s=s.replace(needle,replacement,1)

# Retain survival length in each archived subject's stats.
needle="p.alive=false;p.dead=true;p.shield=0;log('<b>'+esc(p.name)+'</b> terminated · silhouette archived.')"
replacement="p.alive=false;p.dead=true;p.shield=0;p.stats=p.stats||{};p.stats.roundsSurvived=Math.max(0,state.round-1);log('<b>'+esc(p.name)+'</b> terminated · silhouette archived.')"
assert needle in s
s=s.replace(needle,replacement,1)

# Show local subject's debrief when the trial ends, including an all-terminated result.
needle="const survivors=state.players.filter(p=>p.alive),hasWinner=state.phase==='ended'&&survivors.length===1;if(!hasWinner)"
replacement="const survivors=state.players.filter(p=>p.alive),hasWinner=state.phase==='ended'&&survivors.length===1,showDebrief=state.phase==='ended';$('#trialDebrief').classList.toggle('hidden',!showDebrief);if(showDebrief){const subject=state.players.find(p=>p.id===me?.id),st=subject?.stats||{};$('#debriefSubject').textContent=subject?subject.name:'SUBJECT RECORD UNAVAILABLE';$('#debriefResult').textContent=subject?.alive?'SURVIVOR VERIFIED':'SUBJECT TERMINATED';$('#debriefBreakout').textContent=st.breakoutOrder?'#'+st.breakoutOrder+' / '+state.players.length:'NO BREACH';$('#debriefRounds').textContent=String(st.roundsSurvived||0);$('#debriefHits').textContent=String(st.hits||0);$('#debriefCombat').textContent=(st.specialAttacks||0)+' · '+(st.blocks||0);$('#debriefEscapes').textContent=(st.escapesClear||0)+' · '+(st.escapesFailed||0)}if(!hasWinner)"
assert needle in s
s=s.replace(needle,replacement,1)

# Debrief remains compact, in the same corner as the turn timer.
css='''\n.trialDebrief{position:absolute;z-index:6;top:10px;right:10px;width:min(228px,calc(100% - 20px));max-height:42%;overflow:auto;padding:10px 12px;background:rgba(7,17,29,.94);border:1px solid #52717b;box-shadow:0 8px 26px #0009;backdrop-filter:blur(7px);color:#dce9ed}.debriefHead{display:flex;align-items:center;justify-content:space-between;gap:8px}.debriefHead .eyebrow{font-size:8px}.debriefHead strong{font:700 9px 'IBM Plex Mono',monospace;color:#8df4df;text-align:right}.debriefSubject{margin:8px 0 6px;font:700 12px 'Barlow Condensed',sans-serif;letter-spacing:.08em;color:#fff}.debriefGrid{display:grid;grid-template-columns:1fr auto;gap:5px 10px;font:8px 'IBM Plex Mono',monospace}.debriefGrid span{color:#94aab3}.debriefGrid b{color:#e6f1f3;text-align:right}@media(max-width:560px){.trialDebrief{top:6px;right:6px;width:min(195px,calc(100% - 12px));max-height:43%;padding:8px 9px}.debriefGrid{font-size:7px;gap:4px 7px}.debriefSubject{font-size:11px}}\n'''
assert '</style>' in s
s=s.replace('</style>',css+'</style>',1)

p.write_text(s,encoding='utf-8')
print('Updated trial debrief and outcome cues.')
