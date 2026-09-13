"""Make browser-ready copies; retain the supplied rollout files unchanged."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess, json, hashlib
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'static/media'
OUT.mkdir(exist_ok=True)

def run(args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

def prepare(src):
    rel = src.relative_to(ROOT).as_posix()
    key = hashlib.sha256(rel.encode()).hexdigest()[:12]
    video, poster = OUT / (key+'.mp4'), OUT / (key+'.jpg')
    if not video.exists():
        run(['ffmpeg','-y','-i',str(src),'-map','0:v:0','-an','-c:v','libx264','-preset','fast','-crf','25','-pix_fmt','yuv420p','-threads','2','-movflags','+faststart',str(video)])
    if not poster.exists():
        run(['ffmpeg','-y','-ss','0.5','-i',str(src),'-frames:v','1','-vf','scale=640:-2','-q:v','3',str(poster)])
    parts = src.relative_to(ROOT / 'static/videos').parts
    return {'source':rel,'group':parts[0],'method':parts[1] if parts[0]=='page5_comparison' else None,'camera':parts[-2],'src':video.relative_to(ROOT).as_posix(),'poster':poster.relative_to(ROOT).as_posix()}

sources = sorted((ROOT / 'static/videos').glob('page*/*/*.mp4')) + sorted((ROOT / 'static/videos/page5_comparison').glob('*/*/*.mp4'))
with ThreadPoolExecutor(max_workers=3) as pool:
    entries = list(pool.map(prepare, sources))
(ROOT / 'static/media/manifest.json').write_text(json.dumps(entries,indent=2)+'\n')
run(['ffmpeg','-y','-ss','65','-i',str(ROOT/'static/videos/Teaser.mp4'),'-frames:v','1','-vf','scale=1920:-2','-q:v','2',str(OUT/'teaser-poster.jpg')])
run(['ffmpeg','-y','-i',str(ROOT/'static/videos/Teaser.mp4'),'-map','0:v:0','-c','copy','-movflags','+faststart',str(OUT/'teaser.mp4')])
print(f'Prepared {len(entries)} rollouts; {sum(p.stat().st_size for p in OUT.iterdir()) / 1024**2:.1f} MiB')
