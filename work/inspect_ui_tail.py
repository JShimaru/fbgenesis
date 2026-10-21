from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8');i=s.index("$('#moveControls').classList.toggle('hidden'");print(s[i:i+900])
