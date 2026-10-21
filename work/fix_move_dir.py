from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')
old="state=null,moveChoice='wait',myAction=null"
new="state=null,moveChoice='wait',moveDir={x:0,y:-1},myAction=null"
if old not in s: raise SystemExit('Expected state declaration not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
