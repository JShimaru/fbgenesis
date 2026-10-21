from pathlib import Path
p=Path('outputs/index.html')
s=p.read_text(encoding='utf-8')
js_start=s.rfind('<script')
js_end=s.rfind('</script>')
js=s[js_start:js_end]
start=js.find('function positionWinningDebrief(')
end=js.find('function updateUI()',start)
assert start>=0 and end>start
helper="""function positionTrialDebrief(mode,players){const wrap=$('#arenaWrap'),panel=$('#trialDebrief'),classes=['debrief-corner-tl','debrief-corner-tr','debrief-corner-bl','debrief-corner-br','debrief-center'];wrap.classList.remove(...classes,'debrief-extinction');panel.style.top='';if(panel.classList.contains('hidden'))return;if(mode==='extinct'){wrap.classList.add('debrief-extinction');const modal=$('#extinctionOverlay .modal'),wr=wrap.getBoundingClientRect(),mr=modal.getBoundingClientRect();panel.style.top=Math.max(8,mr.bottom-wr.top+8)+'px';return}if(mode!=='winner')return;const wr=wrap.getBoundingClientRect(),cr=cv.getBoundingClientRect(),pw=panel.offsetWidth,ph=panel.offsetHeight,pad=10,items=(players||[]).filter(p=>p.alive||p.dead).map(p=>{const x=cr.left-wr.left+p.x*cr.width/W,y=cr.top-wr.top+p.y*cr.height/H;return p.dead?{l:x-50,r:x+50,t:y-24,b:y+31}:{l:x-43,r:x+43,t:y-37,b:y+24}}),places=[{name:classes[0],l:pad,t:pad},{name:classes[1],l:wr.width-pw-pad,t:pad},{name:classes[2],l:pad,t:wr.height-ph-pad},{name:classes[3],l:wr.width-pw-pad,t:wr.height-ph-pad},{name:classes[4],l:(wr.width-pw)/2,t:(wr.height-ph)/2}];let best=places[0],bestScore=Infinity;for(const c of places){const box={l:c.l,r:c.l+pw,t:c.t,b:c.t+ph};let covered=0,area=0;for(const item of items){const w=Math.max(0,Math.min(box.r,item.r)-Math.max(box.l,item.l)),h=Math.max(0,Math.min(box.b,item.b)-Math.max(box.t,item.t)),overlap=w*h;if(overlap>0){covered++;area+=overlap}}const score=covered*100000+area;if(score<bestScore){bestScore=score;best=c}}wrap.classList.add(best.name)}"""
js=js[:start]+helper+js[end:]
needle="positionWinningDebrief(Boolean(hasWinner&&subject?.alive),state.players)"
assert needle in js
js=js.replace(needle,"",1)
needle="$('#arenaWrap').classList.toggle('extinct',state.phase==='ended'&&survivors.length===0);"
replacement=needle+"positionTrialDebrief(hasWinner?'winner':survivors.length===0&&state.phase==='ended'?'extinct':'fixed',state.players);"
assert needle in js
js=js.replace(needle,replacement,1)
needle="positionWinningDebrief(Boolean(self?.alive),state.players)"
assert needle in js
js=js.replace(needle,"positionTrialDebrief(self?.alive?'winner':'fixed',state.players)",1)
s=s[:js_start]+js+s[js_end:]
css="""
#arenaWrap.debrief-center #trialDebrief{top:50%!important;left:50%!important;right:auto!important;bottom:auto!important;transform:translate(-50%,-50%)!important}
#arenaWrap.debrief-extinction #extinctionOverlay{place-items:start center;padding-top:clamp(10px,4%,24px)}
#arenaWrap.debrief-extinction #extinctionOverlay .modal{max-height:42%;overflow:auto;padding:14px}
#arenaWrap.debrief-extinction #trialDebrief{left:50%!important;right:auto!important;bottom:auto!important;transform:translateX(-50%)!important;max-height:34%;padding:8px 10px}
@media(max-width:560px){#arenaWrap.debrief-extinction #trialDebrief{max-height:33%;padding:7px 8px}}
"""
assert '</style>' in s
s=s.replace('</style>',css+'</style>',1)
p.write_text(s,encoding='utf-8')
print('Added center placement and centered extinction debrief.')
