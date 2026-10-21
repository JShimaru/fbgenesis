from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')
s=s.replace('<div class="banner" id="banner">CONTAINMENT ACTIVE · BREAK GLASS TO BEGIN</div>', '<div class="banner" id="banner">CONTAINMENT ACTIVE · TAP TO BREAK YOUR POD</div><div class="breakoutPrompt hidden" id="breakoutPrompt"><span class="eyebrow">CONTAINMENT BREACH</span><strong>BREAK THE GLASS</strong><p>Strike your pod repeatedly before the purge.</p><div class="glassTrack"><i id="glassProgress"></i></div><button id="breakGlassBtn" class="primary">STRIKE THE GLASS</button></div>')
s=s.replace('<div class="controls moveControls" id="moveControls" style="display:none"', '<div class="controls moveControls hidden" id="moveControls"')
s=s.replace("breakClicks=0,localPod=0,roundTimer", "breakClicks=0,localPod=0,localPodMax=0,roundTimer")
s=s.replace("$('#alarm').classList.toggle('on',state.started);", "$('#alarm').classList.toggle('on',state.started);let self=state.players.find(p=>p.id===me?.id);$('#breakoutPrompt').classList.toggle('hidden',!(state.phase==='breakout'&&self?.contained));")
s=s.replace("$('#moveControls').style.display=state.started&&state.phase==='move'?'grid':'none';", "$('#moveControls').classList.toggle('hidden',!(state.started&&state.phase==='move'));" )
s=s.replace("localPod=30+Math.floor(Math.random()*16);state.players.forEach", "localPod=30+Math.floor(Math.random()*16);localPodMax=localPod;state.players.forEach",1)
s=s.replace("if(state.phase==='breakout'&&prior!=='breakout')localPod=30+Math.floor(Math.random()*16);", "if(state.phase==='breakout'&&prior!=='breakout'){localPod=30+Math.floor(Math.random()*16);localPodMax=localPod}")
old="function selectDirection(x,y){"
new="function breakGlass(){if(!state?.started||state.phase!=='breakout')return;let p=state.players.find(x=>x.id===me?.id);if(!p?.contained)return;breakClicks++;localPod--;$('#glassProgress').style.width=(100*(localPodMax-localPod)/localPodMax)+'%';if(localPod<=0){sendHost({type:'breakout'});breakClicks=0}}function selectDirection(x,y){"
s=s.replace(old,new,1)
old="cv.addEventListener('pointerdown',e=>{if(!state?.started)return;let p=state.players.find(x=>x.id===me?.id);if(state.phase==='breakout'&&p?.contained){breakClicks++;localPod--;if(localPod<=0){sendHost({type:'breakout'});breakClicks=0}return}if(state.phase==='move'&&p?.alive&&!p.contained){"
new="$('#breakGlassBtn').onclick=breakGlass;cv.addEventListener('pointerdown',e=>{if(!state?.started)return;let p=state.players.find(x=>x.id===me?.id);if(state.phase==='breakout'&&p?.contained){breakGlass();return}if(state.phase==='move'&&p?.alive&&!p.contained){"
if old not in s: print('canvas handler replacement not found')
else: s=s.replace(old,new,1)
css='''.breakoutPrompt{position:absolute;z-index:3;left:50%;bottom:14px;transform:translateX(-50%);width:min(430px,calc(100% - 28px));padding:14px 16px;border:1px solid #79909a;background:#07111bea;box-shadow:0 8px 30px #000a;display:grid;gap:6px;text-align:center}.breakoutPrompt>strong{font:800 24px 'Barlow Condensed',sans-serif;letter-spacing:.08em;color:#f2f8fb}.breakoutPrompt p{margin:0 0 3px;font-size:10px;color:#a8bbc4}.breakoutPrompt button{min-height:48px;font-size:14px;letter-spacing:.1em}.glassTrack{height:6px;background:#263641;border:1px solid #3c515e;margin:2px 0 5px}.glassTrack i{display:block;height:100%;width:0;background:linear-gradient(90deg,#54f3e1,#f3cd5a);box-shadow:0 0 10px #54f3e1;transition:width .08s}
+@media(max-width:600px){.breakoutPrompt{bottom:8px;padding:10px}.breakoutPrompt>strong{font-size:21px}.breakoutPrompt p{font-size:9px}}
+'''
s=s.replace('.turnbar{margin-top:12px;',css+'.turnbar{margin-top:12px;',1)
p.write_text(s,encoding='utf-8')
