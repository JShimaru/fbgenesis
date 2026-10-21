from pathlib import Path
s=Path('outputs/index.html').read_text(encoding='utf-8');script=s.rsplit('<script',1)[1].split('>',1)[1].split('</script>',1)[0];Path('work/game-inline.js').write_text(script,encoding='utf-8')
