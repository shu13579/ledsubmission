"""Validate uploads and, if RGB intermediates exist, measure codec error."""
from pathlib import Path
import json
from PIL import Image
ROOT=Path(__file__).resolve().parent
report=[]
paths=sorted((ROOT/'submissions').glob('*.gif'))
assert len(paths)==3, 'Exactly three uploads expected'
for path in paths:
    rawpath=ROOT/'work'/'rgb'/f'{path.stem}.rgb'
    raw=rawpath.read_bytes() if rawpath.exists() else None
    with Image.open(path) as gif:
        assert gif.size==(64,64), (path,gif.size)
        assert path.stat().st_size<5_000_000, path
        assert 40<=gif.n_frames<=96, (path,gif.n_frames)
        assert gif.info.get('loop')==0, 'Must loop forever'
        frames=[]; error=0; durations=[]
        tick=0
        for i in range(gif.n_frames):
            gif.seek(i); durations.append(gif.info['duration'])
            assert gif.info['duration']>=80 and gif.info['duration']%80==0
            pixels=gif.convert('RGB').tobytes()
            # GIF writers may coalesce identical frames; compare on the 80ms timeline.
            for _ in range(gif.info['duration']//80):
                frames.append(pixels)
                if raw:
                    expected=raw[tick*12288:(tick+1)*12288]
                    error+=sum(abs(a-b) for a,b in zip(pixels,expected))
                tick+=1
        assert tick==96 and sum(durations)==7680
        assert len(set(frames))>40, 'Animation must have distinct moving frames'
        # Check the wrap is similar in scale to an ordinary animation step.
        distance=lambda a,b: sum(abs(x-y) for x,y in zip(a,b))/len(a)
        ordinary=[distance(frames[i],frames[i+1]) for i in range(len(frames)-1)]
        seam=distance(frames[-1],frames[0])
        assert seam<=max(ordinary)*1.6+0.1, 'Unexpected loop discontinuity'
        item=dict(file=path.name,width=64,height=64,frames=gif.n_frames,
                  duration_ms=sum(durations),bytes=path.stat().st_size,
                  mean_rgb_error=round(error/(len(frames)*12288),3) if raw else None,
                  loop_seam_mean_rgb_change=round(seam,3),status='PASS')
        report.append(item)
(ROOT/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
for item,result in zip(manifest,report):
    item.update(frames=result['frames'],bytes=result['bytes'])
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
