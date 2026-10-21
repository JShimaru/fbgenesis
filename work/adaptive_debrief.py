from pathlib import Path
p=Path('outputs/index.html')
s=p.read_text(encoding='utf-8')

needle='function updateUI(){if(!state)return;'
helper="function positionWinningDebrief(isWinner,players){const wrap=$('#arenaWrap'),panel=$('#trialDebrief'),classes=['debrief-corner-tl','debrief-corner-tr','debrief-corner-bl','debrief-corner-br'];wrap.classList.remove(...classes);if(!isWinner||panel.classList.contains('hidden'))return;const wr=wrap.getBoundingClientRect(),cr=cv.getBoundingClientRect(),pw=panel.offsetWidth,ph=panel.offsetHeight,pad=10,items=(players||[]).filter(p=>p.alive||p.dead).map(p=>{const x=cr.left-wr.left+p.x*cr.width/W,y=cr.top-wr.top+p.y*cr.height/H;return p.dead?{l:x-50,r:x+50,t:y-24,b:y+31}:{l:x-43,r:x+43,t:y-37,b:y+24}}),corners=[{name:classes[0],l:pad,t:pad},{name:classes[1],l:wr.width-pw-pad,t:pad},{name:classes[2],l:pad,t:wr.height-ph-pad},{name:classes[3],l:wr.width-pw-pad,t:wr.height-ph-pad}];let best=corners[0],bestScore=Infinity;for(const c of corners){const box={l:c.l,r:c.l+pw,t:c.t,b:c.t+ph};let covered=0,area=0;for(const item of items){const w=Math.max(0,Math.min(box.r,item.r)-Math.max(box.l,item.l)),h=Math.max(0,Math.min(box.b,item.b)-Math.max(box.t,item.t)),overlap=w*h;if(overlap>0){covered++;area+=overlap}}const score=covered*100000+area;if(score<bestScore){bestScore=score;best=c}}wrap.classList.add(best.name)}function updateUI(){if(!state)return;"
assert needle in s
s=s.replace(needle,helper,1)
needle="$('#debriefEscapes').textContent=(st.escapesClear||0)+' · '+(st.escapesFailed||0)}if(!hasWinner)"
replacement="$('#debriefEscapes').textContent=(st.escapesClear||0)+' · '+(st.escapesFailed||0);positionWinningDebrief(Boolean(hasWinner&&subject?.alive),state.players)}if(!hasWinner)"
assert needle in s
s=s.replace(needle,replacement,1)
css='''\n#arenaWrap.debrief-corner-tl #trialDebrief{top:10px!important;right:auto!important;bottom:auto!important;left:10px!important}#arenaWrap.debrief-corner-tr #trialDebrief{top:10px!important;right:10px!important;bottom:auto!important;left:auto!important}#arenaWrap.debrief-corner-bl #trialDebrief{top:auto!important;right:auto!important;bottom:10px!important;left:10px!important}#arenaWrap.debrief-corner-br #trialDebrief{top:auto!important;right:10px!important;bottom:10px!important;left:auto!important}@media(max-width:560px){#arenaWrap.debrief-corner-tl #trialDebrief,#arenaWrap.debrief-corner-tr #trialDebrief{top:6px!important}#arenaWrap.debrief-corner-bl #trialDebrief,#arenaWrap.debrief-corner-br #trialDebrief{bottom:6px!important}#arenaWrap.debrief-corner-tl #trialDebrief,#arenaWrap.debrief-corner-bl #trialDebrief{left:6px!important}#arenaWrap.debrief-corner-tr #trialDebrief,#arenaWrap.debrief-corner-br #trialDebrief{right:6px!important}}\n'''
assert '</style>' in s
s=s.replace('</style>',css+'</style>',1)
# Re-evaluate the winning panel after viewport changes so it stays clear for screenshots.
needle="$('#newGame').onclick=()=>{if(host)restartTrial();else sendHost({type:'restart'})};"
replacement="window.addEventListener('resize',()=>{if(state?.phase==='ended'&&state.players.filter(p=>p.alive).length===1){const self=state.players.find(p=>p.id===me?.id);positionWinningDebrief(Boolean(self?.alive),state.players)}});$('#newGame').onclick=()=>{if(host)restartTrial();else sendHost({type:'restart'})};"
assert needle in s
s=s.replace(needle,replacement,1)
p.write_text(s,encoding='utf-8')
print('Added winner-only adaptive debrief placement.')
