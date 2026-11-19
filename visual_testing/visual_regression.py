"""Screenshot baseline and pixel-difference utilities (requires Pillow)."""
from pathlib import Path
from PIL import Image, ImageChops

ROOT=Path(__file__).resolve().parent
BASELINES=ROOT/'baselines'; ACTUAL=ROOT/'actual'; DIFFS=ROOT/'diffs'
for folder in (BASELINES,ACTUAL,DIFFS): folder.mkdir(parents=True,exist_ok=True)

def capture(page, name, baseline=False):
    folder=BASELINES if baseline else ACTUAL; path=folder/f'{name}.png'
    page.screenshot(path=str(path),full_page=True); return path

def compare(name, threshold=0.0):
    base=BASELINES/f'{name}.png'; actual=ACTUAL/f'{name}.png'
    if not base.exists() or not actual.exists(): raise FileNotFoundError('Capture both baseline and actual screenshots first.')
    a=Image.open(base).convert('RGBA'); b=Image.open(actual).convert('RGBA')
    if a.size != b.size: return {'match':False,'reason':'image dimensions differ','baseline_size':a.size,'actual_size':b.size,'difference_ratio':1.0}
    diff=ImageChops.difference(a,b); changed=sum(1 for px in diff.get_flattened_data() if px != (0,0,0,0)); ratio=changed/(a.width*a.height)
    diff.save(DIFFS/f'{name}_diff.png')
    return {'match':ratio <= threshold,'difference_ratio':round(ratio,6),'threshold':threshold,'diff_path':str(DIFFS/f'{name}_diff.png')}
