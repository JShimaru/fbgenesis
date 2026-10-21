from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')
old="state.breakoutCount=0;state.siteNetwork=makeTrialSiteNetwork();state.mistDepth=0;state.players.forEach(p=>{p.mistExposure=0;"
new="state.breakoutCount=0;state.siteNetwork=makeTrialSiteNetwork();state.mistDepth=0;state.mistPotential=0;state.mistExpansion=0;state.players.forEach(p=>{p.mistExposure=0;"
assert old in s;s=s.replace(old,new,1)
old="p.threshold=-(2+Math.floor(Math.random()*9));"
new="p.threshold=-(5+Math.floor(Math.random()*8));"
assert old in s;s=s.replace(old,new,1)
old="function recoverWhileStill(p){const used=Math.max(0,Number(p.restHealUsed)||0),gain=Math.max(0,Math.min(4,20-used,100-p.breath));"
new="function recoverWhileStill(p){const used=Math.max(0,Number(p.restHealUsed)||0),gain=Math.max(0,Math.min(6,20-used,100-p.breath));"
assert old in s;s=s.replace(old,new,1)
old="state.round++;state.mistDepth=Math.max(0,(state.round-14)*45);if(state.round===15)log('ENVIRONMENTAL WARNING: Perimeter mist release initiated.');state.deadline=Date.now()+4000;"
new="state.round++;state.mistExpansion=mistExpansionAtRound(state.round);state.mistDepth=state.mistExpansion*45;state.mistPotential=state.round<10?0:state.round<13?2:state.round<16?4:8;if(state.round===10)log('ENVIRONMENTAL WARNING: Perimeter mist release initiated.');if(state.round===16)log('ENVIRONMENTAL WARNING: Mist toxicity at critical potential.');state.deadline=Date.now()+4000;"
assert old in s;s=s.replace(old,new,1)
# The expansion cadence is 3 rounds until the 8-damage exposure tier, then 2, then the final fill on the next round.
needle="function beginMove(){if(!host)return;"
replacement="function mistExpansionAtRound(round){if(round<10)return 0;if(round<13)return 1;if(round<16)return 2;if(round<18)return 3;if(round<20)return 4;if(round<21)return 5;return 6}function beginMove(){if(!host)return;"
assert needle in s;s=s.replace(needle,replacement,1)
old="if(p.alive&&p.breath<=p.threshold){p.alive=false;"
new="if(p.alive&&(p.breath<=p.threshold||p.breath<=-12)){p.alive=false;"
assert old in s;s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Updated mist timing, collapse thresholds, and recovery rate.')
