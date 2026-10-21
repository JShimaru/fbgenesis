from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')
for action,key in [('block','D'),('attack','A'),('special','S'),('escape','F')]:
 old=f'data-action="{action}" aria-pressed="false"'
 new=f'data-action="{action}" aria-pressed="false" aria-keyshortcuts="{key}"'
 assert old in s,old
 s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Added keyboard shortcut metadata for assistive technology.')
