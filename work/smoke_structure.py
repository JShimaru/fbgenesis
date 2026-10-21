from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8')
checks={
'Controls moved inside map':'<div class="arena-wrap" id="arenaWrap">' in s and s.index('<div class="turnbar hidden"') < s.index('<div class="bottom">'),
'Extinction overlay wired':'id="extinctionOverlay"' in s and "$('#extinctionOverlay').classList.toggle" in s,
'Reinitialize action wired':"function restartTrial()" in s and "$('#reinitiateBtn').onclick" in s,
'All-dead purge resolves':'checkDeaths();if(!checkWinner())beginMove();' in s,
'No stale accidental CSS rule':'+@media' not in s}
for k,v in checks.items():print(k, 'PASS' if v else 'FAIL')
if not all(checks.values()):raise SystemExit(1)
