from pathlib import Path
p=Path('work/smoke_solo.js');s=p.read_text(encoding='utf-8')
old="if(human.breath!==74)throw new Error('Stillness recovery did not resume after travel')"
new="if(human.breath!==76)throw new Error('Stillness recovery did not resume after travel')"
assert old in s
p.write_text(s.replace(old,new,1),encoding='utf-8')
print('Updated smoke expectation for the new recovery amount.')
