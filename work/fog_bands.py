from pathlib import Path
p=Path('outputs/index.html');s=p.read_text(encoding='utf-8')
start=s.find('function drawMistLayer(){');end=s.find('function draw(){',start)
assert start>=0 and end>start
new="function drawMistLayer(){if(!state||!(state.mistDepth>0))return;const depth=Math.min(Math.max(W,H),state.mistDepth),left=20,right=W-20,top=20,bottom=H-20,segments=8,band=depth/segments;cx.save();for(let i=0;i<segments;i++){cx.fillStyle='rgba(151,177,178,'+(0.045-i*.003)+')';cx.fillRect(left+i*band,top,band+1,bottom-top);cx.fillRect(right-(i+1)*band,top,band+1,bottom-top);cx.fillRect(left,top+i*band,right-left,band+1);cx.fillRect(left,bottom-(i+1)*band,right-left,band+1)}cx.globalAlpha=.7;cx.strokeStyle='rgba(201,223,219,.24)';cx.lineWidth=2;const front=Math.min(depth,Math.min(right-left,bottom-top)/2);cx.strokeRect(left+front,top+front,Math.max(0,right-left-front*2),Math.max(0,bottom-top-front*2));if(depth>=(bottom-top)/2){cx.fillStyle='rgba(137,160,164,.22)';cx.fillRect(left,top,right-left,bottom-top)}cx.restore()}"
s=s[:start]+new+s[end:]
p.write_text(s,encoding='utf-8')
print('Replaced gradient fog with layered haze bands.')
