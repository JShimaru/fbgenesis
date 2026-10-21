from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8')
a=s.index('.turnbar{');b=s.index('</style>',a);print(s[b-2200:b])
