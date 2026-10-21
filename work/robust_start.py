from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')
s=s.replace("$('#beginProtocol').classList.toggle('hidden',!host);$('#lobbyTitle').textContent=host?'SUBJECTS IN CONTAINMENT':'AWAITING HOST AUTHORIZATION';$('#lobbyHelp').textContent=host?'Initiate the protocol when you are ready to begin.':'The host will begin the trial shortly.';", "$('#beginProtocol').classList.toggle('hidden',!host);$('#beginProtocol').disabled=!(host&&state.players.length>=2&&!state.started);$('#lobbyTitle').textContent=host?'SUBJECTS IN CONTAINMENT':'AWAITING HOST AUTHORIZATION';$('#lobbyHelp').textContent=host?`${state.players.length} subjects ready. Initiate the protocol when you are ready.`:'The host will begin the trial shortly.';")
old="function startGame(){if(!host||state.players.length<2)return;state.started=true;state.phase='breakout';"
new="function startGame(){if(!state||state.phase!=='lobby')return;if(!host||state.players.length<2){$('#lobbyHelp').textContent='At least two subjects are needed to initiate the protocol.';log('Protocol is waiting for more subjects.');return}state.started=true;state.phase='breakout';"
if old not in s: print('startGame prefix not found')
else:s=s.replace(old,new,1)
s=s.replace("$('#startOverlay').classList.add('hidden');sendState()}function addBots", "$('#startOverlay').classList.add('hidden');sendState();draw()}function addBots",1)
s=s.replace("$('#beginProtocol').onclick=startGame;", "$('#beginProtocol').onclick=()=>{startGame();draw()};")
p.write_text(s,encoding='utf-8')
