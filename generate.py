"""Original 64x64 LED art. No external artwork, prompts, or API keys required."""
from pathlib import Path
import argparse
import json
import math
import random
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
N, DELAY = 96, 80
TAU = math.tau

def mix(a, b, t):
    return tuple(round(x*(1-t)+y*t) for x,y in zip(a,b))

def star(d,x,y,c,large=False):
    d.point((x,y),fill=c)
    if large:
        d.line((x-1,y,x+1,y),fill=c)
        d.line((x,y-1,x,y+1),fill=c)

STARS = [(random.Random(i*71+8).randrange(64),random.Random(i*31+4).randrange(64),i) for i in range(42)]

def sky(t):
    im=Image.new('RGB',(64,64),(4,6,19)); d=ImageDraw.Draw(im)
    for x,y,k in STARS:
        v=(math.sin(TAU*t+k)+1)/2
        star(d,x,y,[(22,31,58),(58,78,110),(138,174,195)][min(2,int(v*3))],k%13==0 and v>.8)
    return im,d

def jelly(t):
    im,d=sky(t)
    # A distant ringed planet makes the creature read as a space traveller.
    d.ellipse((45,8,56,19),fill=(67,43,113))
    d.arc((41,10,60,18),0,190,fill=(122,94,172),width=1)
    d.arc((46,9,54,16),180,280,fill=(148,114,185),width=1)
    bob=round(2*math.sin(TAU*t)); cx=28; cy=23+bob
    # Long ribbons, gently curling with a continuous phase at the loop seam.
    for k,x0 in enumerate([17,22,27,32,37]):
        pts=[]
        length=[18,24,21,25,19][k]
        for q in range(length):
            x=round(x0+math.sin(TAU*t+q*.32+k*.8)*(1+q*.11))
            pts.append((x,cy+9+q))
        d.line(pts,fill=(36,45,91),width=3)
        d.line(pts,fill=[(58,212,218),(105,115,247),(244,108,199),(117,144,255),(56,224,223)][k])
        for q in range(3,length,7):
            if (q+k+int(t*12))%3==0: d.point(pts[q],fill=(240,217,255))
    pulse=math.sin(TAU*t)
    rx=16+round(pulse); ry=13
    # Pixel-stepped dome with a luminous rim and internal curved ribs.
    for y in range(cy-ry,cy+6):
        for x in range(cx-rx,cx+rx+1):
            yy=(y-cy)/ry; xx=(x-cx)/rx
            if xx*xx+yy*yy<=1 and y<=cy+5:
                radial=math.sqrt(xx*xx+yy*yy)
                c=(36,40,103)
                if radial>.88: c=(62,193,214)
                elif radial>.70: c=(42,102,156)
                elif y<cy-5: c=(59,65,145)
                if abs(xx)<.19: c=(75,95,177)
                d.point((x,y),fill=c)
    d.arc((cx-rx+3,cy-ry+3,cx+rx-3,cy+8),185,330,fill=(134,245,241),width=1)
    d.arc((cx-8,cy-ry+4,cx+8,cy+12),185,340,fill=(150,124,235),width=1)
    d.line((cx-rx+2,cy+4,cx+rx-2,cy+4),fill=(160,243,244),width=1)
    for x in range(cx-rx+3,cx+rx-1,4):
        d.rectangle((x,cy+5,x+1,cy+6),fill=(111,108,218))
    d.ellipse((cx-5,cy-1,cx+5,cy+3),fill=(227,115,216))
    d.line((cx-3,cy,cx+3,cy),fill=(255,210,244))
    for k in range(6):
        a=TAU*t+k*1.73
        x=round(28+26*math.cos(a)); y=round(34+20*math.sin(a))
        if 0<=x<64 and 0<=y<64: star(d,x,y,(52,144,160),k==2)
    return im

def cat_city(t):
    im=Image.new('RGB',(64,64),(8,9,25));d=ImageDraw.Draw(im)
    d.ellipse((40,5,51,16),fill=(132,150,174))
    d.ellipse((43,3,54,14),fill=(8,9,25))
    # Silhouette skyline and tiny lit windows.
    for k,(x,y,w) in enumerate([(0,17,9),(10,23,9),(20,10,10),(34,19,7),(44,24,10),(56,13,8)]):
        d.rectangle((x,y,x+w,43),fill=(16,20,43))
        d.line((x,y,x+w,y),fill=(30,35,59))
        for yy in range(y+4,40,6):
            for xx in range(x+2,x+w,4):
                if (xx+yy+k)%4!=0: d.rectangle((xx,yy,xx+1,yy+1),fill=(71,63,90))
    # A fictional rooftop noodle shop: hand-drawn bowl instead of tiny text.
    d.rectangle((3,26,22,44),fill=(35,23,49))
    d.rectangle((4,27,21,39),outline=(229,76,164))
    d.rectangle((6,29,19,37),fill=(27,20,44))
    d.arc((8,30,17,36),0,180,fill=(255,173,185),width=2)
    d.line((8,32,17,32),fill=(255,173,185))
    for x in (10,13,16):
        off=round(math.sin(TAU*t+x))
        d.line((x,31,x+off,29),fill=(125,74,105))
    d.rectangle((47,27,57,41),fill=(22,26,46),outline=(47,204,218))
    for y in (30,33,36):d.line((50,y,54,y),fill=(57,120,155))
    # Drizzle wraps offscreen; all drops travel an integer distance per cycle.
    for k in range(27):
        x=(k*23+int(t*16))%72-4; y=(k*17+int(t*64))%64
        if y<44: d.line((x,y,x-1,y+2),fill=(32,53,80))
    d.rectangle((0,44,63,63),fill=(13,18,33))
    d.line((0,44,63,44),fill=(54,64,83));d.line((0,46,63,46),fill=(25,36,52))
    for y in range(49,64,3):
        offset=round(2*math.sin(TAU*t+y))
        d.line((5+offset,y,18+offset,y),fill=(80,31,68))
        d.line((47-offset,y,55-offset,y),fill=(23,72,85))
    # Rounded seated cat, warm eyes, swaying tail, occasional blink.
    tail=[(39,43),(44,43),(47,40),(47+round(2*math.sin(TAU*t)),36)]
    d.line(tail,fill=(77,82,108),width=3)
    d.line([(x,y-1) for x,y in tail],fill=(111,114,140))
    d.ellipse((28,33,42,45),fill=(77,82,108))
    d.ellipse((29,25,42,37),fill=(100,105,133))
    d.polygon([(29,29),(29,22),(34,26)],fill=(117,120,149))
    d.polygon([(37,26),(42,22),(42,30)],fill=(117,120,149))
    d.polygon([(30,25),(30,28),(32,27)],fill=(210,126,151))
    d.polygon([(39,27),(41,25),(41,28)],fill=(210,126,151))
    blink=.45<t<.49
    for x in (32,38):
        d.line((x,30,x+1,30),fill=(253,202,107))
        if not blink:d.point((x,31),fill=(253,202,107))
    d.point((35,33),fill=(241,153,173))
    d.line((29,34,32,34),fill=(165,164,188));d.line((39,34,43,34),fill=(165,164,188))
    d.rectangle((32,36,38,37),fill=(225,71,144));d.point((37,38),fill=(255,203,103))
    d.line((29,44,33,44),fill=(142,143,163));d.line((36,44,40,44),fill=(142,143,163))
    # Soft reflection under the cat.
    for y,w in [(49,7),(52,5),(55,3)]:
        x=35+round(math.sin(TAU*t+y))
        d.line((x-w,y,x+w,y),fill=(39,43,62))
    return im

LEAVES=[(x,y,random.Random(x*77+y).random()) for y in range(11,31) for x in range(14,49)
        if ((x-27)/14)**2+((y-21)/9)**2<1 or ((x-40)/9)**2+((y-22)/7)**2<1]

def garden(t):
    im,d=sky(t)
    # Four smooth seasonal palettes, returning exactly to spring.
    season=t*4; idx=int(season)%4; f=max(0,(season%1-.75)*4); f=f*f*(3-2*f)
    colors=[((247,132,184),(142,60,117)),((93,222,158),(30,110,100)),
            ((255,181,80),(175,64,60)),((196,225,245),(95,125,160))]
    bright=mix(colors[idx][0],colors[(idx+1)%4][0],f)
    dark=mix(colors[idx][1],colors[(idx+1)%4][1],f)
    # Compact planet: lit grassy cap, rocky curved underside, orbiting moon.
    d.ellipse((12,32,52,58),fill=(36,41,70))
    d.ellipse((14,32,50,54),fill=(57,64,92))
    d.ellipse((12,32,52,42),fill=(49,113,116))
    d.arc((12,32,52,42),180,360,fill=(123,213,176),width=2)
    for x,y in [(21,46),(36,49),(29,54),(44,43),(16,42)]:
        d.rectangle((x,y,x+2,y+1),fill=(77,88,112))
    d.arc((7,34,57,61),0,180,fill=(51,89,118),width=1)
    # Wind-sculpted tree and roots.
    d.line([(31,37),(33,31),(32,26),(28,22),(25,19)],fill=(159,111,101),width=3)
    d.line([(33,31),(39,26),(42,20)],fill=(159,111,101),width=2)
    d.line([(32,27),(35,21),(34,15)],fill=(159,111,101),width=2)
    d.line([(25,38),(31,36),(39,38)],fill=(159,111,101),width=2)
    d.ellipse((13,12,40,29),fill=dark)
    d.ellipse((29,14,48,29),fill=dark)
    for x,y,v in LEAVES:
        # Deliberate stippling gives foliage texture at the actual LED resolution.
        if v<.22:continue
        xx=x+round(math.sin(TAU*t+y*.22)*.7)
        d.point((xx,y),fill=bright if v>.53 else dark)
        if v>.94:d.point((xx,y-1),fill=mix(bright,(255,246,214),.45))
    # Seasonal petals / fireflies / autumn leaves / snow move on a closed orbit.
    for k in range(12):
        q=(t+k/12)%1
        x=round(11+43*q+3*math.sin(TAU*t+k));y=round(23+28*q)
        if not (12<x<51 and 32<y<59):
            star(d,x%64,y,bright,k%5==0)
    a=TAU*t-.7
    x=round(32+27*math.cos(a)); y=round(40+16*math.sin(a))
    d.ellipse((x-2,y-2,x+2,y+2),fill=(171,195,212));d.point((x-1,y-1),fill=(238,241,224))
    return im

ARTS=[('01-cosmic-jellyfish','Cosmic Jellyfish',jelly),
      ('02-neon-cat','Neon Rain / Rooftop Cat',cat_city),
      ('03-orbital-seasons','Orbital Seasons',garden)]

def generate(export_rgb=False):
    out=ROOT/'submissions'; preview=ROOT/'previews'
    out.mkdir(exist_ok=True);preview.mkdir(exist_ok=True)
    summary=[]; posters=[]
    for stem,title,draw in ARTS:
        frames=[draw(i/N) for i in range(N)]
        if export_rgb:
            raw=ROOT/'work'/'rgb';raw.mkdir(parents=True,exist_ok=True)
            (raw/f'{stem}.rgb').write_bytes(b''.join(im.tobytes() for im in frames))
        # A single stable palette prevents shimmer from per-frame quantization.
        atlas=Image.new('RGB',(64*12,64*8))
        for i,im in enumerate(frames):atlas.paste(im,((i%12)*64,(i//12)*64))
        palette=atlas.quantize(colors=128,method=Image.Quantize.MEDIANCUT)
        indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
        path=out/f'{stem}.gif'
        indexed[0].save(path,save_all=True,append_images=indexed[1:],duration=DELAY,loop=0,optimize=False,disposal=1)
        frames[N//8].save(preview/f'{stem}.png')
        large=[im.resize((512,512),Image.Resampling.NEAREST) for im in indexed]
        large[0].save(preview/f'{stem}-512.gif',save_all=True,append_images=large[1:],duration=DELAY,loop=0,optimize=False,disposal=1)
        posters.append(frames[N//8])
        summary.append({'file':path.name,'title':title,'width':64,'height':64,'frames':N,'frame_ms':DELAY,'loop_ms':N*DELAY,'bytes':path.stat().st_size})
    contact=Image.new('RGB',(512*3,512),(4,6,19))
    for i,im in enumerate(posters):contact.paste(im.resize((512,512),Image.Resampling.NEAREST),(i*512,0))
    contact.save(preview/'contact-sheet.png')
    (ROOT/'manifest.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--export-rgb',action='store_true')
    generate(p.parse_args().export_rgb)
