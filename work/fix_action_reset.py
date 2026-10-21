from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')
s=s.replace("function updateUI(){if(!state)return;if(state.phase==='move'", "function updateUI(){if(!state)return;if(state.phase==='combat'&&uiPhase!=='combat'){document.querySelectorAll('[data-action]').forEach(b=>{b.disabled=false;b.classList.remove('sel');b.setAttribute('aria-pressed','false')})}uiPhase=state.phase;if(state.phase==='move'",1)
p.write_text(s,encoding='utf-8')
