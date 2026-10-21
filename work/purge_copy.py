from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')
s=s.replace('<p>Strike your pod repeatedly before the purge.</p><div class="glassTrack">', '<p>Strike your pod repeatedly before the purge.</p><span class="purgeClock" id="purgeClock">AWAITING FIRST BREACH</span><div class="glassTrack">')
s=s.replace("$('#breakoutPrompt').classList.toggle('hidden',!(state.phase==='breakout'&&self?.contained));", "$('#breakoutPrompt').classList.toggle('hidden',!(state.phase==='breakout'&&self?.contained));$('#purgeClock').textContent=state.purgeAt?'SYSTEM PURGE IN '+String(Math.max(0,Math.ceil((state.purgeAt-Date.now())/1000))).padStart(2,'0'):'SYSTEM PURGE STARTS AT FIRST BREACH';")
s=s.replace('.breakoutPrompt>strong{font:800 24px', '.purgeClock{font-size:9px;color:var(--amber);letter-spacing:.1em}.breakoutPrompt>strong{font:800 24px')
p.write_text(s,encoding='utf-8')
