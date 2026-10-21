from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')

# Accessible, opt-in sound control in the header.
needle='<button class="controlSideBtn" id="controlSideBtn" type="button" aria-pressed="false" aria-label="Move panel position: right">MOVE PANEL: RIGHT</button>'
replacement=needle+'<button class="controlSideBtn audioToggle" id="audioToggle" type="button" aria-pressed="false" aria-label="Enable ambient audio and sound effects">AUDIO: OFF</button>'
assert needle in s;s=s.replace(needle,replacement,1)

# Place keyboard hints visibly on the combat buttons.
changes={
'<strong>GUARD</strong>Brace against incoming strikes':'<strong>GUARD <kbd>D</kbd></strong>Brace against incoming strikes',
'<strong>STRIKE</strong>A focused blow at one opponent':'<strong>STRIKE <kbd>A</kbd></strong>A focused blow at one opponent',
'<strong>SIGNATURE</strong>A sweeping attack against every opponent':'<strong>SIGNATURE <kbd>S</kbd></strong>A sweeping attack against every opponent',
'<strong>ESCAPE</strong>Run clear of the engagement':'<strong>ESCAPE <kbd>F</kbd></strong>Run clear of the engagement'
}
for a,b in changes.items():
 assert a in s,a
 s=s.replace(a,b,1)

# Top-center translucent combat choices keep the arena visible around the action.
css="""
.overlay#combatOverlay:not(.targetingEscape){z-index:8;pointer-events:none;place-items:start center;padding:10px 8px;background:transparent}
.overlay#combatOverlay:not(.targetingEscape) .modal{pointer-events:auto;width:min(340px,calc(100% - 16px));max-width:340px;max-height:45%;overflow:auto;margin:0;padding:12px 14px;background:rgba(7,17,29,.91);border-color:#54727b;box-shadow:0 8px 28px #0009;backdrop-filter:blur(7px)}
.overlay#combatOverlay:not(.targetingEscape) .modal h2{font-size:24px;margin:3px 0 4px}
.overlay#combatOverlay:not(.targetingEscape) .modal p{font-size:9px;line-height:1.45;margin:4px 0}
.overlay#combatOverlay:not(.targetingEscape) .timer{font-size:18px;margin:2px auto}
.overlay#combatOverlay:not(.targetingEscape) .combatActions{gap:5px;margin-top:7px}
.overlay#combatOverlay:not(.targetingEscape) .control{min-height:54px;padding:6px 8px;font-size:8px;line-height:1.35}
.combatActions .control strong{display:flex;align-items:center;justify-content:space-between;gap:8px;font-size:10px}
.combatActions kbd{min-width:18px;padding:2px 4px;border:1px solid #58717a;border-radius:3px;background:#0b2029;color:#bffcf2;text-align:center;font:700 8px 'IBM Plex Mono',monospace}
.audioToggle[aria-pressed="true"]{color:#a8fff0;border-color:#59b7ad;box-shadow:0 0 9px #59f0df33}
@media(max-width:560px){.overlay#combatOverlay:not(.targetingEscape){padding:6px}.overlay#combatOverlay:not(.targetingEscape) .modal{width:min(290px,calc(100% - 12px));padding:9px 10px;max-height:40%}.overlay#combatOverlay:not(.targetingEscape) .modal h2{font-size:20px}.overlay#combatOverlay:not(.targetingEscape) .modal p{font-size:8px}.overlay#combatOverlay:not(.targetingEscape) .control{min-height:48px}.audioToggle{font-size:7px!important;padding:5px 6px!important}}
"""
assert '</style>' in s;s=s.replace('</style>',css+'</style>',1)

js_start=s.rfind('<script');js_end=s.rfind('</script>');js=s[js_start:js_end]
needle="logLines=[],uiPhase='',uiRound=0;const W=1000,H=595;"
replacement="logLines=[],uiPhase='',uiRound=0,audioEnabled=false,audioCtx=null,audioMaster=null,ambientOscillators=[],lastAudioEventKey='',lastRareVoiceId=null;const W=1000,H=595;"
assert needle in js;js=js.replace(needle,replacement,1)

# Host-authored rare log fragments are shared with every client; audio playback is opt-in and local.
needle='function updateUI(){if(!state)return;'
audio="""function ensureAudioContext(){if(audioCtx)return true;const AudioCtor=window.AudioContext||window.webkitAudioContext;if(!AudioCtor)return false;try{audioCtx=new AudioCtor();return true}catch{return false}}function startAmbient(){if(!audioEnabled||!ensureAudioContext()||ambientOscillators.length)return;try{audioCtx.resume?.();audioMaster=audioCtx.createGain();audioMaster.gain.value=.22;audioMaster.connect(audioCtx.destination);[[48,'sine',.12],[72,'triangle',.045],[96,'sine',.018]].forEach(([frequency,type,volume])=>{const osc=audioCtx.createOscillator(),gain=audioCtx.createGain();osc.type=type;osc.frequency.value=frequency;gain.gain.value=volume;osc.connect(gain);gain.connect(audioMaster);osc.start();ambientOscillators.push(osc)})}catch{}}function stopAmbient(){ambientOscillators.forEach(osc=>{try{osc.stop()}catch{}try{osc.disconnect()}catch{}});ambientOscillators=[];if(audioMaster){try{audioMaster.disconnect()}catch{}audioMaster=null}}function soundCue(type,kind){if(!audioEnabled||!audioCtx)return;const presets=type==='strike'?[185,78,.13,'triangle',.09]:type==='block'?[720,470,.1,'square',.045]:type==='escape'?[360,130,.2,'sawtooth',.045]:type==='mist-hit'?[92,47,.32,'sine',.07]:kind==='lightning'?[760,130,.22,'sawtooth',.065]:kind==='gust'?[280,85,.24,'triangle',.055]:kind==='soundwaves'?[430,760,.3,'sine',.05]:null;if(!presets)return;try{const [from,to,duration,wave,volume]=presets,osc=audioCtx.createOscillator(),gain=audioCtx.createGain(),now=audioCtx.currentTime;osc.type=wave;osc.frequency.setValueAtTime(from,now);osc.frequency.exponentialRampToValueAtTime(Math.max(35,to),now+duration);gain.gain.setValueAtTime(.0001,now);gain.gain.exponentialRampToValueAtTime(volume,now+.012);gain.gain.exponentialRampToValueAtTime(.0001,now+duration);osc.connect(gain);gain.connect(audioMaster||audioCtx.destination);osc.start(now);osc.stop(now+duration+.02)}catch{}}function speakRareObservation(text){if(!audioEnabled||typeof SpeechSynthesisUtterance==='undefined'||!window.speechSynthesis)return;try{window.speechSynthesis.cancel();const voice=new SpeechSynthesisUtterance(text);voice.rate=.86;voice.pitch=.68;voice.volume=.48;window.speechSynthesis.speak(voice)}catch{}}function syncAudioFromState(){if(!state)return;const events=state.visualEffects||[],key=events.map((e,i)=>[e.at,e.type,e.kind||'',e.target?.x??'',e.target?.y??'',i].join(':')).join('|');if(key&&key!==lastAudioEventKey){lastAudioEventKey=key;events.forEach(e=>{if(['strike','special','block','escape','mist-hit'].includes(e.type))soundCue(e.type,e.kind)})}else if(!key)lastAudioEventKey='';const rare=state.rareVoiceLine;if(rare&&rare.id!==lastRareVoiceId){lastRareVoiceId=rare.id;speakRareObservation(rare.text)}}function setAudioEnabled(enabled){if(enabled&&!ensureAudioContext()){audioEnabled=false;$('#audioToggle').textContent='AUDIO UNAVAILABLE';$('#audioToggle').setAttribute('aria-pressed','false');return}audioEnabled=enabled;$('#audioToggle').textContent='AUDIO: '+(enabled?'ON':'OFF');$('#audioToggle').setAttribute('aria-pressed',String(enabled));$('#audioToggle').setAttribute('aria-label',enabled?'Disable ambient audio and sound effects':'Enable ambient audio and sound effects');if(enabled){startAmbient();if(state?.rareVoiceLine)speakRareObservation(state.rareVoiceLine.text)}else{stopAmbient();if(window.speechSynthesis)window.speechSynthesis.cancel()}}function logRareObservation(){if(!host||!state||state.round<3||Math.random()>.1)return;const lines=['ARCHIVE NOTE: The oldest route has no recorded destination.','VOICE CACHE: That cadence appears in records predating this facility.','SUBROUTINE: A breath was counted after its subject stopped.','ENGINEERING NOTE: No one remembers drawing this symbol.','UNLISTED FEED: The arena was here before the building.','RECOVERY CACHE: Four breaths found where none were recorded.'],text=lines[Math.floor(Math.random()*lines.length)];state.rareVoiceLine={id:Date.now()+Math.random(),text};log(text)}function updateUI(){if(!state)return;syncAudioFromState();"""
assert needle in js;js=js.replace(needle,audio,1)

# Add rare lines occasionally into the host-synced observation log.
needle='state.deadline=Date.now()+4000;logLoreFragment();for(const p of state.players.filter'
replacement='state.deadline=Date.now()+4000;logLoreFragment();logRareObservation();for(const p of state.players.filter'
assert needle in js;js=js.replace(needle,replacement,1)

# Combat A/S/D/F while preserving movement keys and escape route navigation.
needle="if(state?.phase!=='move')return;if(state?.phase!=='move')return;let dirs={"
replacement="if(state?.phase!=='move')return;if(state?.phase!=='move')return;if(isEngaged(p)&&!escapeSelecting){const combatKey={a:'attack',A:'attack',s:'special',S:'special',d:'block',D:'block',f:'escape',F:'escape'}[e.key];if(combatKey){e.preventDefault();const button=[...document.querySelectorAll('[data-action]')].find(b=>b.dataset.action===combatKey);if(button&&!button.disabled)button.click();return}}let dirs={"
assert needle in js;js=js.replace(needle,replacement,1)

# Wire the opt-in audio switch.
needle="$('#controlSideBtn').onclick=()=>{const left=$('#arenaWrap').classList.toggle('controls-left');$('#controlSideBtn').textContent='MOVE PANEL: '+(left?'LEFT':'RIGHT');$('#controlSideBtn').setAttribute('aria-pressed',String(left));$('#controlSideBtn').setAttribute('aria-label','Move panel position: '+(left?'left':'right'))};"
replacement=needle+"$('#audioToggle').onclick=()=>setAudioEnabled(!audioEnabled);"
assert needle in js;js=js.replace(needle,replacement,1)
s=s[:js_start]+js+s[js_end:]
p.write_text(s,encoding='utf-8')
print('Added combat visibility, A/S/D/F input, opt-in audio, and rare lab log/voice lines.')
