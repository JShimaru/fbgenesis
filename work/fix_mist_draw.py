from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')
old='bottom=H-20;cX=0;cx.save()'
assert old in s
p.write_text(s.replace(old,'bottom=H-20;cx.save()',1),encoding='utf-8')
print('Removed an unintended drawing variable.')
