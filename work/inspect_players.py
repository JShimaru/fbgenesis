from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8')
i=s.index("$('#players').innerHTML")
print(s[i:i+500])
