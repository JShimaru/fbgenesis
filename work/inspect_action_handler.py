from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8');q="document.querySelectorAll('[data-action]')";i=s.index(q,s.index('function makeLobby'));print(s[i:i+800])
