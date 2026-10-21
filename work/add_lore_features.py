from pathlib import Path
p=Path('outputs/index.html')
s=p.read_text(encoding='utf-8')

# Add restrained ancient geometry to the aura ring.
needle="function draw(){cx.clearRect(0,0,W,H);"
replacement="function drawAncientAura(x,y,color){cx.save();cx.globalAlpha=.24;cx.strokeStyle=color;cx.lineWidth=.8;cx.beginPath();cx.ellipse(x,y,17,7,0,0,Math.PI*2);cx.stroke();for(let i=0;i<8;i++){const a=i*Math.PI/4,px=x+Math.cos(a)*17,py=y+Math.sin(a)*7,tx=x+Math.cos(a+.18)*11,ty=y+Math.sin(a+.18)*4.5;cx.beginPath();cx.moveTo(px,py);cx.lineTo(tx,ty);cx.lineTo(x+Math.cos(a+.36)*17,y+Math.sin(a+.36)*7);cx.stroke()}cx.beginPath();cx.moveTo(x-5,y);cx.lineTo(x,y-2.2);cx.lineTo(x+5,y);cx.lineTo(x,y+2.2);cx.closePath();cx.stroke();cx.restore()}function draw(){cx.clearRect(0,0,W,H);"
assert needle in s
s=s.replace(needle,replacement,1)
needle="cx.ellipse(p.x,p.y+12,17,7,0,0,Math.PI*2);cx.stroke();cx.restore();if(p.shield)"
replacement="cx.ellipse(p.x,p.y+12,17,7,0,0,Math.PI*2);cx.stroke();cx.restore();drawAncientAura(p.x,p.y+12,col);if(p.shield)"
assert needle in s
s=s.replace(needle,replacement,1)

# A brief global network log, emitted by the host every other round and synced to clients.
needle="function beginMoveRound(){if(!host)return;state.phase='move';state.combatTurn=0;state.fighters=[];state.moves={};state.actions={};state.paths={};state.round++;state.deadline=Date.now()+4000;"
replacement="function logLoreFragment(){if(!host||!state||state.round%2!==0)return;const entries=['SYSTEM WARNING: Subject bio-rhythm incompatible with Anima Protocol.','NETWORK UPDATE: Syncing trial data with Site 04 [Giza] and Site 12 [Teotihuacan].','DATA LOG: Scanning for dormant ancient genetic markers... Negative.','DIRECTIVE: Continue automated trials until natural technique manifestation is detected.'];log(entries[Math.floor(Math.random()*entries.length)])}function beginMoveRound(){if(!host)return;state.phase='move';state.combatTurn=0;state.fighters=[];state.moves={};state.actions={};state.paths={};state.round++;state.deadline=Date.now()+4000;logLoreFragment();"
assert needle in s
s=s.replace(needle,replacement,1)

# Add distinct ancient motifs to existing special attack effects.
needle="cx.strokeStyle='#fff';cx.lineWidth=1;cx.stroke()}\n    else if(e.kind==='gust')"
replacement="cx.strokeStyle='#fff';cx.lineWidth=1;cx.stroke();cx.globalAlpha=.45*fade;cx.strokeStyle='#bfefff';cx.lineWidth=1;cx.beginPath();cx.moveTo(t.x-9,t.y-4);cx.lineTo(t.x-4,t.y-4);cx.lineTo(t.x-4,t.y);cx.lineTo(t.x+2,t.y);cx.lineTo(t.x+2,t.y+4);cx.lineTo(t.x+8,t.y+4);cx.stroke()}\n    else if(e.kind==='gust')"
assert needle in s
s=s.replace(needle,replacement,1)
needle="cx.quadraticCurveTo((e.from.x+t.x)/2+k*12,(e.from.y+t.y)/2-22+(progress*18),t.x,t.y+k*5);cx.stroke()}}\n    else{for(let k=0;k<3;k++){cx.strokeStyle=k===0?'#e1fcff':'#8ee4f0';cx.lineWidth=2;cx.beginPath();cx.arc(t.x,t.y,7+progress*36+k*5,0,Math.PI*2);cx.stroke()}}"
replacement="cx.quadraticCurveTo((e.from.x+t.x)/2+k*12,(e.from.y+t.y)/2-22+(progress*18),t.x,t.y+k*5);cx.stroke()}cx.save();cx.translate((e.from.x+t.x)/2,(e.from.y+t.y)/2);cx.rotate(progress*Math.PI*2);cx.strokeStyle='#b9ffe9';cx.lineWidth=1.2;for(let n=0;n<3;n++){const r=6+n*5;cx.strokeRect(-r,-r,r*2,r*2);cx.beginPath();cx.moveTo(-r,-r);cx.lineTo(r,r);cx.moveTo(r,-r);cx.lineTo(-r,r);cx.stroke()}cx.restore()}\n    else{for(let k=0;k<3;k++){cx.strokeStyle=k===0?'#e1fcff':'#8ee4f0';cx.lineWidth=2;cx.beginPath();cx.arc(t.x,t.y,7+progress*36+k*5,0,Math.PI*2);cx.stroke()}cx.globalAlpha=.48*fade;cx.strokeStyle='#d8faff';cx.lineWidth=1.1;const gy=t.y+progress*18;cx.beginPath();cx.moveTo(t.x-7,gy);cx.quadraticCurveTo(t.x,gy-6,t.x+7,gy);cx.quadraticCurveTo(t.x,gy+6,t.x-7,gy);cx.stroke();cx.beginPath();cx.arc(t.x,gy,2,0,Math.PI*2);cx.stroke();cx.beginPath();cx.moveTo(t.x,gy-9);cx.lineTo(t.x+3,gy-6);cx.lineTo(t.x,gy-3);cx.lineTo(t.x-3,gy-6);cx.closePath();cx.stroke()}"
assert needle in s
s=s.replace(needle,replacement,1)

# Append victory-only periodic fracture styling. Glyphs only appear during a very short pulse.
needle='</style>'
css="""
.victoryBanner.loreGlitch{isolation:isolate;overflow:hidden}
.victoryBanner.loreGlitch h2{animation:victoryFracture 3.8s infinite steps(1,end)}
.victoryBanner.loreGlitch::after{content:'𓂀 𓋹 𓊹 𓁹';position:absolute;inset:0;display:grid;place-items:center;color:#d9fff2;font:700 18px/1 'IBM Plex Mono',monospace;letter-spacing:.8em;opacity:0;pointer-events:none;mix-blend-mode:screen;animation:glyphFracture 3.8s infinite steps(1,end)}
@keyframes victoryFracture{0%,88%,91%,100%{text-shadow:none;transform:none;filter:none}89%{text-shadow:-2px 0 #ff5364,2px 0 #55f4df;transform:translateX(1px);filter:contrast(1.5)}90%{text-shadow:2px 0 #ff5364,-2px 0 #55f4df;transform:translateX(-1px);filter:contrast(1.8)}}
@keyframes glyphFracture{0%,88%,91%,100%{opacity:0;clip-path:inset(50% 0 50%)}89%{opacity:.2;clip-path:inset(18% 0 72%)}90%{opacity:.13;clip-path:inset(68% 0 16%)}}
@media(prefers-reduced-motion:reduce){.victoryBanner.loreGlitch h2,.victoryBanner.loreGlitch::after{animation:none}.victoryBanner.loreGlitch::after{display:none}}
"""
assert needle in s
s=s.replace(needle,css+needle,1)
# Mark the winner surface so the effect is limited to the victory state.
needle="$('#winnerName').textContent=survivors[0].name;if(!victoryNoticeStarted)"
replacement="$('#winnerName').textContent=survivors[0].name;$('#victoryBanner').classList.add('loreGlitch');if(!victoryNoticeStarted)"
assert needle in s
s=s.replace(needle,replacement,1)
needle="$('#victoryBanner').classList.add('hidden');$('#continueBtn').classList.add('hidden')}else"
replacement="$('#victoryBanner').classList.add('hidden');$('#victoryBanner').classList.remove('loreGlitch');$('#continueBtn').classList.add('hidden')}else"
assert needle in s
s=s.replace(needle,replacement,1)

p.write_text(s,encoding='utf-8')
print('Updated lore details in',p)
