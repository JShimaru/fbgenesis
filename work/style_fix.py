from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8').replace('.moveControls{display:none!important;grid-template-columns:', '.moveControls{display:grid;grid-template-columns:')
p.write_text(s,encoding='utf-8')
