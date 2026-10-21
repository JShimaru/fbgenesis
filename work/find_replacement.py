from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8')
print('replacement chars',s.count('\ufffd'))
for i,c in enumerate(s):
 if c=='\ufffd': print(repr(s[max(0,i-45):i+45]))
