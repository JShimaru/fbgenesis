from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')
s=s.replace("document.querySelectorAll('[data-action]').forEach(x=>x.disabled=true)});$('#continueBtn')", "document.querySelectorAll('[data-action]').forEach(x=>x.disabled=true)};$('#continueBtn')",1)
p.write_text(s,encoding='utf-8')
