"""Independently decode Jixoo GIFs, compare every pixel with source RGB."""
from pathlib import Path
import json, statistics, math
from generate import flight_pose
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parent
reports=[]
poses=[flight_pose(i/128) for i in range(128)]
assert all(b[0]>=a[0] for a,b in zip(poses,poses[1:])), 'Aircraft moves backwards'
assert all(abs(p[2])<=math.radians(20)+1e-9 for p in poses), 'Aircraft pitch exceeds 20 degrees'
assert max(abs(b[2]-a[2]) for a,b in zip(poses,poses[1:]))<math.radians(2), 'Abrupt aircraft rotation'
assert poses[0][0]+6<0 and poses[-1][0]-6>63, 'Visible loop reset'
distances=[math.hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(poses,poses[1:]) if 0<a[3]<b[3]<1]
assert max(distances)/min(distances)<1.01, 'Uneven aircraft speed'
for meta in json.loads((ROOT/'manifest.json').read_text(encoding='utf-8')):
    p=ROOT/meta['file'];im=Image.open(p)
    assert im.size==(64,64) and p.stat().st_size<5_000_000
    assert im.info.get('loop')==0 and im.n_frames==128
    raw=(ROOT/'work/rgb'/f'{p.stem}.rgb').read_bytes()
    frames=[];colors=set();duration=0
    for i in range(im.n_frames):
        im.seek(i);f=im.convert('RGB');frames.append(f.copy())
        assert im.info['duration']==80
        duration+=im.info['duration'];data=f.tobytes();colors.update(zip(data[0::3],data[1::3],data[2::3]))
        assert f.tobytes()==raw[i*12288:(i+1)*12288],f'Color mismatch in {p.name} frame {i}'
    assert len(colors)<=128
    changes=[sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)/3 for a,b in zip(frames,frames[1:])]
    seam=sum(ImageStat.Stat(ImageChops.difference(frames[-1],frames[0])).mean)/3
    assert seam<=max(changes)*1.5+0.1,(p.name,seam,max(changes))
    report=dict(file=p.name,bytes=p.stat().st_size,frames=len(frames),duration_ms=duration,
        unique_colors=len(colors),exact_rgb_match=True,loop_seam_mean_rgb_difference=round(seam,3),
        max_normal_frame_difference=round(max(changes),3),passed=True)
    if p.name.startswith('01-'):
        report['flight_checks']={'forward_only':True,'constant_speed':True,'pitch_limit_degrees':20,
            'max_rotation_per_frame_degrees':round(max(abs(b[2]-a[2]) for a,b in zip(poses,poses[1:]))*180/math.pi,3),
            'loop_reset_offscreen':True}
    reports.append(report)
(ROOT/'validation.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
print(json.dumps(reports,indent=2))
