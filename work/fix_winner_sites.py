from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')
# The winner's location is adaptive only on that winner's own client.
old="positionTrialDebrief(hasWinner?'winner':survivors.length===0&&state.phase==='ended'?'extinct':'fixed',state.players);"
new="const debriefSubject=state.players.find(player=>player.id===me?.id);positionTrialDebrief(hasWinner&&debriefSubject?.alive?'winner':survivors.length===0&&state.phase==='ended'?'extinct':'fixed',state.players);"
assert old in s
s=s.replace(old,new,1)
# Trial-specific balanced site network, with three numerology-linked site numbers.
needle="function startGame(){if(!state||state.phase!=='lobby')return;"
generator="function makeTrialSiteNetwork(){const pools={EGYPTIAN:['Giza Necropolis','Karnak Temple Complex','Abu Simbel'],'AZTEC':['Teotihuacan','Templo Mayor, Tenochtitlan','Tenochtitlan Causeways'],'GREEK':['Acropolis of Athens','Temple of Apollo, Delphi','Olympia Sanctuary']},cultures=Object.keys(pools),count=4+Math.floor(Math.random()*5),shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a},chosen=cultures.map(c=>({culture:c,name:pools[c][Math.floor(Math.random()*pools[c].length)]})),remaining=shuffle(cultures.flatMap(c=>pools[c].filter(name=>!chosen.some(site=>site.name===name)).map(name=>({culture:c,name}))));chosen.push(...remaining.slice(0,count-chosen.length));const significant=shuffle([7,13,22,33,72,108,144,216,333,432,777]).slice(0,3),ids=[...significant],used=new Set(ids);while(ids.length<count){const n=1+Math.floor(Math.random()*999);if(!used.has(n)){used.add(n);ids.push(n)}}return shuffle(chosen).map((site,i)=>({...site,id:ids[i]}))}function formatTrialSite(site){return 'SITE '+site.id+' ['+site.name+' · '+site.culture+']'}function logNetworkUpdate(){const sites=state?.siteNetwork||[];if(sites.length<2)return;const first=Math.floor(Math.random()*sites.length);let second=Math.floor(Math.random()*(sites.length-1));if(second>=first)second++;log('NETWORK UPDATE: '+sites.length+' remote sites linked // '+formatTrialSite(sites[first])+' · '+formatTrialSite(sites[second])+'.')}"
assert needle in s
s=s.replace(needle,generator+needle,1)
needle="state.breakoutCount=0;state.players.forEach(p=>{p.stats="
replacement="state.breakoutCount=0;state.siteNetwork=makeTrialSiteNetwork();state.players.forEach(p=>{p.stats="
assert needle in s
s=s.replace(needle,replacement,1)
needle="log('Protocol initiated. Subjects are in containment.');sendState();"
replacement="log('Protocol initiated. Subjects are in containment.');logNetworkUpdate();sendState();"
assert needle in s
s=s.replace(needle,replacement,1)
old="function logLoreFragment(){if(!host||!state||state.round%2!==0)return;const entries=['SYSTEM WARNING: Subject bio-rhythm incompatible with Anima Protocol.','NETWORK UPDATE: Syncing trial data with Site 04 [Giza] and Site 12 [Teotihuacan].','DATA LOG: Scanning for dormant ancient genetic markers... Negative.','DIRECTIVE: Continue automated trials until natural technique manifestation is detected.'];log(entries[Math.floor(Math.random()*entries.length)])}"
new="function logLoreFragment(){if(!host||!state||state.round%2!==0)return;const entries=[()=>log('SYSTEM WARNING: Subject bio-rhythm incompatible with Anima Protocol.'),()=>logNetworkUpdate(),()=>log('DATA LOG: Scanning for dormant ancient genetic markers... Negative.'),()=>log('DIRECTIVE: Continue automated trials until natural technique manifestation is detected.')];entries[Math.floor(Math.random()*entries.length)]()}"
assert old in s
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Fixed local-winner placement and randomized each trial’s site network.')
