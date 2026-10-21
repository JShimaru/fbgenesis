from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')
css='''.combatActions{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:12px}.combatActions .control{min-height:78px}.escapeControls{display:grid;gap:10px;margin-top:14px}.escapeControls>p{margin:0;color:#a8bbc4;font-size:10px;line-height:1.6}.escapeDistances,.escapeDirs,.escapeButtons{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px}.escapeDistances button,.escapeDirs button,.escapeButtons button{min-height:44px;padding:8px;font-size:10px}.escapeDirs{grid-template-columns:repeat(2,minmax(0,1fr))}.escapeDistances button.sel,.escapeDirs button.sel{border-color:var(--cyan);background:#123239;color:var(--cyan)}.escapeButtons{grid-template-columns:1fr 1fr}.escapeButtons .primary{background:#0f3a3b}.overlay#combatOverlay{background:#030910b8}.arena-wrap .modal{max-height:calc(100% - 32px);overflow:auto}
+@media(max-width:560px){.combatActions{gap:6px}.combatActions .control{min-height:64px;padding:8px}.combatActions .control strong{font-size:15px}.escapeDistances button,.escapeDirs button,.escapeButtons button{min-height:48px;font-size:9px;padding:6px}.arena-wrap .modal{padding:16px;max-width:calc(100% - 24px)}}
+'''
s=s.replace('</style>',css.replace('\n+@media','\n@media')+'</style>',1)
p.write_text(s,encoding='utf-8')
