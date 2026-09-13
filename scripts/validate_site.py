"""Validate the static publication and its actual media, without dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json, subprocess, struct
ROOT = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.refs=[]; self.videos=0; self.sources=[]; self.images=0
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        for key in ('src','href','poster','aria-controls','aria-labelledby'):
            if key in attrs: self.refs.append((key,attrs[key]))
        if tag=='video':
            self.videos+=1
            assert 'controls' in attrs and 'playsinline' in attrs and attrs.get('preload')=='none'
            assert 'autoplay' not in attrs
        if tag=='source': self.sources.append(attrs['src'])
        if tag=='img': self.images+=1; assert attrs.get('alt')
page=Page(); content=(ROOT/'index.html').read_text(); page.feed(content)
assert len(page.ids)==len(set(page.ids)), 'Duplicate HTML IDs'
for key,ref in page.refs:
    if key in ('aria-controls','aria-labelledby'):
        assert ref in page.ids, ref; continue
    url=urlsplit(ref)
    if url.scheme or url.netloc: continue
    if url.path: assert (ROOT/unquote(url.path)).is_file(), ref
    if url.fragment: assert url.fragment in page.ids, ref
assert page.videos==40, page.videos
manifest=json.loads((ROOT/'static/media/manifest.json').read_text())
assert len(manifest)==33
assert len({m['src'] for m in manifest})==33
for m in manifest:
    assert m['src'] in page.sources
    assert (ROOT/m['poster']).exists()
for src in page.sources:
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=codec_name,pix_fmt,width,height:format=duration','-of','json',str(ROOT/src)]))
    stream=data['streams'][0]
    assert stream['codec_name']=='h264', src
    assert stream['pix_fmt']=='yuv420p', src
    assert float(data['format']['duration'])>0, src
    if src.startswith('static/media/'):
        atoms=[]
        with (ROOT/src).open('rb') as file:
            while header:=file.read(8):
                size,kind=struct.unpack('>I4s',header); atoms.append(kind)
                if size==0: break
                assert size>=8
                file.seek(size-8,1)
        assert atoms.index(b'moov') < atoms.index(b'mdat'), src
pdf=subprocess.check_output(['pdftotext',str(ROOT/'static/paper.pdf'),'-'],text=True)
assert 'Action-Flow Consistency Across Views' in pdf
assert '26 of 40' in pdf and '12 of 40' in pdf
for stale in ['74.4%', '53.3%', '95.0 ± 4.3', 'RR-PLACEHOLDER', '[TODO:']:
    assert stale not in content
assert 'Pages:           8' in subprocess.check_output(['pdfinfo',str(ROOT/'static/paper.pdf')],text=True)
subprocess.run(['node','--check',str(ROOT/'static/js/project.js')],check=True)
print(f'PASS: {page.videos} playable H.264 videos, all local links and posters, {page.images} paper figures, 33-source manifest, 8-page v6 paper, and JavaScript syntax.')
