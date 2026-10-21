from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')

# Give fog deaths an identifiable archive mark in the arena screenshot.
old="cx.fillStyle='#a74d4e';cx.font='8px IBM Plex Mono';cx.fillText('SUBJECT TERMINATED',-45,27);cx.restore();return}"
new="cx.fillStyle=p.stats?.terminatedInMist?'#c2e0df':'#a74d4e';cx.font='7px IBM Plex Mono';cx.textAlign='center';cx.fillText((p.stats?.terminatedInMist?'MIST // ':'')+p.name.toUpperCase(),0,27);cx.textAlign='left';cx.restore();return}"
assert old in s;s=s.replace(old,new,1)

# Draw a still, expanding haze from all four room edges.
needle='function draw(){cx.clearRect(0,0,W,H);'
func="function drawMistLayer(){if(!state||!(state.mistDepth>0))return;const depth=Math.min(Math.max(W,H),state.mistDepth),left=20,right=W-20,top=20,bottom=H-20;cX=0;cx.save();cx.globalAlpha=.84;let g=cx.createLinearGradient(left,0,left+depth,0);g.addColorStop(0,'rgba(171,193,191,.44)');g.addColorStop(.68,'rgba(143,169,171,.25)');g.addColorStop(1,'rgba(129,154,161,.08)');cx.fillStyle=g;cx.fillRect(left,top,Math.min(depth,right-left),bottom-top);g=cx.createLinearGradient(right,0,right-depth,0);g.addColorStop(0,'rgba(171,193,191,.44)');g.addColorStop(.68,'rgba(143,169,171,.25)');g.addColorStop(1,'rgba(129,154,161,.08)');cx.fillStyle=g;cx.fillRect(Math.max(left,right-depth),top,Math.min(depth,right-left),bottom-top);g=cx.createLinearGradient(0,top,0,top+depth);g.addColorStop(0,'rgba(171,193,191,.42)');g.addColorStop(.68,'rgba(143,169,171,.24)');g.addColorStop(1,'rgba(129,154,161,.08)');cx.fillStyle=g;cx.fillRect(left,top,right-left,Math.min(depth,bottom-top));g=cx.createLinearGradient(0,bottom,0,bottom-depth);g.addColorStop(0,'rgba(171,193,191,.42)');g.addColorStop(.68,'rgba(143,169,171,.24)');g.addColorStop(1,'rgba(129,154,161,.08)');cx.fillStyle=g;cx.fillRect(left,Math.max(top,bottom-depth),right-left,Math.min(depth,bottom-top));if(depth>=(bottom-top)/2){cx.fillStyle='rgba(137,160,164,.2)';cx.fillRect(left,top,right-left,bottom-top)}cx.restore()}function draw(){cx.clearRect(0,0,W,H);"
assert needle in s;s=s.replace(needle,func,1)
# Remove accidental undeclared typo placeholder from function string.
s=s.replace('const depth=Math.min(Math.max(W,H),state.mistDepth),left=20,right=W-20,top=20,bottom=H-20,cX=0;','const depth=Math.min(Math.max(W,H),state.mistDepth),left=20,right=W-20,top=20,bottom=H-20;',1)
needle="o.x+5,o.y+o.h/2+3)});if(!state)return;"
replacement="o.x+5,o.y+o.h/2+3)});drawMistLayer();if(!state)return;"
assert needle in s;s=s.replace(needle,replacement,1)

# Stats are host-owned state and reset once per new trial.
needle="state.breakoutCount=0;state.siteNetwork=makeTrialSiteNetwork();state.players.forEach(p=>{p.stats={breakoutOrder:null,regularAttacks:0,specialAttacks:0,hits:0,blocks:0,escapesClear:0,escapesFailed:0,roundsSurvived:0,impactRounds:0}});"
replacement="state.breakoutCount=0;state.siteNetwork=makeTrialSiteNetwork();state.mistDepth=0;state.players.forEach(p=>{p.mistExposure=0;p.mistCaught=false;p.lastDamageSource=null;p.stats={breakoutOrder:null,regularAttacks:0,specialAttacks:0,hits:0,blocks:0,escapesClear:0,escapesFailed:0,roundsSurvived:0,impactRounds:0,mistRounds:0,terminatedInMist:false}});"
assert needle in s;s=s.replace(needle,replacement,1)

# Fog opens at round 15 and advances one tile per round; stay at a stable depth for the screenshot.
needle="state.round++;state.deadline=Date.now()+4000;logLoreFragment();"
replacement="state.round++;state.mistDepth=Math.max(0,(state.round-14)*45);if(state.round===15)log('ENVIRONMENTAL WARNING: Perimeter mist release initiated.');state.deadline=Date.now()+4000;logLoreFragment();"
assert needle in s;s=s.replace(needle,replacement,1)

# Determine whether an arena location is within the advancing perimeter mist.
needle="function resolveMoves(){if(!host||state.phase!=='move')return;const active=state.players.filter(p=>p.alive&&!p.contained),engaged="
replacement="function isInsideMist(p){const d=Number(state?.mistDepth)||0;return d>0&&(p.x<42.5+d||p.x>957.5-d||p.y<42.5+d||p.y>552.5-d)}function resolveMoves(){if(!host||state.phase!=='move')return;const active=state.players.filter(p=>p.alive&&!p.contained);active.forEach(p=>p.lastDamageSource=null);const engaged="
assert needle in s;s=s.replace(needle,replacement,1)

# Apply doubling per caught round, remembering exposure if a subject escapes and later re-enters.
needle="for(const event of attackEvents){const target=state.players.find(q=>q.id===event.target)"
replacement="for(const p of active.filter(q=>q.alive&&!q.contained)){if(isInsideMist(p)){p.stats=p.stats||{};const exposure=Math.max(0,Number(p.mistExposure)||0),baseDose=2*Math.pow(2,exposure);p.mistExposure=exposure+1;p.stats.mistRounds=(p.stats.mistRounds||0)+1;p.mistCaught=true;let dose=baseDose;if(p.shield>0){const absorbed=Math.min(p.shield,dose);p.shield-=absorbed;dose-=absorbed}if(dose>0){p.breath-=dose;p.lastDamageSource='MIST'}visuals.push({type:'mist-hit',target:{x:p.x,y:p.y}});log('<b>'+esc(p.name)+'</b> caught in perimeter mist · exposure intensifies.')}else p.mistCaught=false}for(const event of attackEvents){const target=state.players.find(q=>q.id===event.target)"
assert needle in s;s=s.replace(needle,replacement,1)

# Create a brief localized smoky pulse on each mist exposure.
needle="}else if(e.type==='outcome'){"
replacement="}else if(e.type==='mist-hit'){cx.globalAlpha=.19*fade;cx.strokeStyle='#c4d7d5';cx.fillStyle='#8ea8a8';cx.lineWidth=2;for(let k=0;k<3;k++){const radius=13+progress*20+k*6;cx.beginPath();cx.arc(e.target.x+Math.sin(k*3+progress*5)*3,e.target.y+Math.cos(k*4+progress*4)*3,radius,0,Math.PI*2);cx.stroke()}for(let k=0;k<5;k++){const px=e.target.x+Math.sin(k*8+progress*6)*10,py=e.target.y+Math.cos(k*7+progress*6)*8;cx.globalAlpha=.1*fade;cx.beginPath();cx.arc(px,py,3+progress*5,0,Math.PI*2);cx.fill()}}else if(e.type==='outcome'){"
assert needle in s;s=s.replace(needle,replacement,1)
# Extend effect duration for the mist puff alongside other short impact cues.
needle="state.visualEffects=visuals.map(v=>({...v,at:Date.now(),duration:1250}));"
replacement="state.visualEffects=visuals.map(v=>({...v,at:Date.now(),duration:v.type==='mist-hit'?1800:1250}));"
assert needle in s;s=s.replace(needle,replacement,1)

# Record fog-specific termination reasons and show it in the end-state debrief.
needle="p.alive=false;p.dead=true;p.shield=0;p.stats=p.stats||{};p.stats.roundsSurvived=Math.max(0,state.round-1);log('<b>'+esc(p.name)+'</b> terminated · silhouette archived.')"
replacement="p.alive=false;p.dead=true;p.shield=0;p.stats=p.stats||{};p.stats.roundsSurvived=Math.max(0,state.round-1);p.stats.terminatedInMist=p.lastDamageSource==='MIST';log(p.stats.terminatedInMist?'<b>'+esc(p.name)+'</b> terminated in the perimeter mist · silhouette archived.':'<b>'+esc(p.name)+'</b> terminated · silhouette archived.')"
assert needle in s;s=s.replace(needle,replacement,1)
needle="$('#debriefResult').textContent=subject?.alive?'SURVIVOR VERIFIED':'SUBJECT TERMINATED';"
replacement="$('#debriefResult').textContent=subject?.alive?'SURVIVOR VERIFIED':st.terminatedInMist?'TERMINATED IN MIST':'SUBJECT TERMINATED';"
assert needle in s;s=s.replace(needle,replacement,1)
needle="<span>ESCAPES CLEAR · FAILED</span><b id=\"debriefEscapes\">—</b>"
replacement="<span>ESCAPES CLEAR · FAILED</span><b id=\"debriefEscapes\">—</b><span>MIST ROUNDS</span><b id=\"debriefMist\">—</b>"
assert needle in s;s=s.replace(needle,replacement,1)
needle="$('#debriefEscapes').textContent=(st.escapesClear||0)+' · '+(st.escapesFailed||0);"
replacement=needle+"$('#debriefMist').textContent=String(st.mistRounds||0);"
assert needle in s;s=s.replace(needle,replacement,1)

# The all-terminated archival state shows the fog filling the full arena; it remains frozen at game end.
needle="function checkWinner(){let alive=state.players.filter(p=>p.alive);if(alive.length<=1){state.phase='ended';"
replacement="function checkWinner(){let alive=state.players.filter(p=>p.alive);if(alive.length<=1){if(alive.length===0)state.mistDepth=Math.max(Number(state.mistDepth)||0,Math.max(W,H));state.phase='ended';"
assert needle in s;s=s.replace(needle,replacement,1)
p.write_text(s,encoding='utf-8')
print('Implemented expanding perimeter mist, escalating exposure, visual cues, and fog outcome records.')
