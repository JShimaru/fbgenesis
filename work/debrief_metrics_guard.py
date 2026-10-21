from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')
old="wrap.classList.remove(...classes,'debrief-extinction');panel.style.top='';if(panel.classList.contains('hidden'))return;if(mode==='extinct'){wrap.classList.add('debrief-extinction');const modal=$('#extinctionOverlay .modal'),wr=wrap.getBoundingClientRect(),mr=modal.getBoundingClientRect();"
new="wrap.classList.remove(...classes,'debrief-extinction');panel.style.top='';if(panel.classList.contains('hidden')||typeof wrap.getBoundingClientRect!=='function')return;if(mode==='extinct'){const modal=$('#extinctionOverlay .modal');if(!modal||typeof modal.getBoundingClientRect!=='function')return;wrap.classList.add('debrief-extinction');const wr=wrap.getBoundingClientRect(),mr=modal.getBoundingClientRect();"
assert old in s
s=s.replace(old,new,1)
old="if(mode!=='winner')return;const wr=wrap.getBoundingClientRect(),cr=cv.getBoundingClientRect(),pw=panel.offsetWidth"
new="if(mode!=='winner'||typeof cv.getBoundingClientRect!=='function')return;const wr=wrap.getBoundingClientRect(),cr=cv.getBoundingClientRect(),pw=panel.offsetWidth"
assert old in s
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Added graceful fallback for test/browser shims without layout metrics.')
