"""Original pixel choreography: 128 frames, 64x64 RGB, no external artwork."""
from pathlib import Path
import math, json, bisect
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
N, DELAY, TAU = 128, 80, math.tau
INK = (5, 9, 22)
FONT = {
'A':['010','101','111','101','101'],'B':['110','101','110','101','110'],
'D':['110','101','101','101','110'],'E':['111','100','110','100','111'],
'F':['111','100','110','100','100'],'G':['111','100','101','101','111'],
'I':['111','010','010','010','111'],'J':['001','001','001','101','010'],
'L':['100','100','100','100','111'],'M':['10001','11011','10101','10001','10001'],
'N':['101','111','111','111','101'],'O':['010','101','101','101','010'],
'P':['110','101','110','100','100'],'R':['110','101','110','101','101'],
'S':['011','100','010','001','110'],'T':['111','010','010','010','010'],
'U':['101','101','101','101','111'],'V':['101','101','101','101','010'],
'W':['10101','10101','10101','10101','01010'],
'X':['101','101','010','101','101'],' ':['0']*5,
'{':['011','010','100','010','011'],'}':['110','010','001','010','110'],
'<':['001','010','100','010','001'],'>':['100','010','001','010','100'],
'/':['001','001','010','100','100']}

def text(d,s,y,color,scale=1,x=None):
    width=sum(len(FONT[c][0])+1 for c in s)*scale-scale
    if x is None: x=(64-width)//2
    for c in s:
        for yy,row in enumerate(FONT[c]):
            for xx,v in enumerate(row):
                if v=='1': d.rectangle((x+xx*scale,y+yy*scale,x+(xx+1)*scale-1,y+(yy+1)*scale-1),fill=color)
        x+=(len(FONT[c][0])+1)*scale

def base(t):
    im=Image.new('RGB',(64,64),INK);d=ImageDraw.Draw(im)
    for y in range(64): d.line((0,y,63,y),fill=(5+int(y/16),9+int(y/8),22+int(y/5)))
    for k in range(24):
        x=(k*19+7)%64;y=(k*13+3)%43
        c=(80,115,142) if math.sin(TAU*t+k)>.65 else (24,41,66)
        d.point((x,y),fill=c)
    return im,d

def sphere(d,x,y,r,c):
    x,y=round(x),round(y)
    d.ellipse((x-r,y-r,x+r,y+r),fill=tuple(int(v*.4) for v in c))
    d.ellipse((x-r+1,y-r+1,x+r-1,y+r-1),fill=c)
    if r>=2:d.point((x-1,y-1),fill=(237,253,255))

def atomium(d,t,cx=48,cy=31,size=11,rotate=False):
    # Eight cube corners plus center. Twelve edges and eight radial tubes.
    a=TAU*t if rotate else .6
    pts=[]
    for x,y,z in [(x,y,z) for x in (-1,1) for y in (-1,1) for z in (-1,1)]+[(0,0,0)]:
        xx=x*math.cos(a)+z*math.sin(a);zz=-x*math.sin(a)+z*math.cos(a)
        yy=y*.82-zz*.46;depth=y*.46+zz*.82
        pts.append((cx+size*xx*.85,cy+size*yy,depth))
    for i in range(8):
        for j in range(i+1,8):
            if (i^j) in (1,2,4):d.line((pts[i][:2],pts[j][:2]),fill=(57,90,112),width=2)
        d.line((pts[i][:2],pts[8][:2]),fill=(81,132,152))
    for k in sorted(range(9),key=lambda k:pts[k][2]):
        x,y,z=pts[k]; sphere(d,x,y,2 if size<13 else 3,(108,187,204) if z<0 else (166,220,226))
    return pts

def flight_route(u):
    """Continuous cubic curve; leave pixel rounding until the final drawing."""
    v=1-u
    return (v**3*(-8)+3*v*v*u*15+3*v*u*u*43+u**3*72,
            v**3*18+u**3*18)

FLIGHT_LENGTH=[0.0]
for k in range(1,513):
    a,b=flight_route((k-1)/512),flight_route(k/512)
    FLIGHT_LENGTH.append(FLIGHT_LENGTH[-1]+math.hypot(b[0]-a[0],b[1]-a[1]))

def flight_pose(t):
    progress=max(0,min(1,(t-.07)/.78))
    distance=progress*FLIGHT_LENGTH[-1]
    k=max(1,min(512,bisect.bisect_left(FLIGHT_LENGTH,distance)))
    fraction=(distance-FLIGHT_LENGTH[k-1])/(FLIGHT_LENGTH[k]-FLIGHT_LENGTH[k-1])
    u=(k-1+fraction)/512;v=1-u
    x,y=flight_route(u)
    dx=3*(v*v*23+2*v*u*28+u*u*29)
    dy=54*(u*u-v*v)
    angle=max(-math.radians(20),min(math.radians(20),math.atan2(dy,dx)))
    return x,y,angle,u

def bridge(t):
    im,d=base(t)
    # Symbolic Japan / Antwerp composition, not a geographic reconstruction.
    # An ocean crossing replaces labels: a restrained dotted arc across the sky.
    for k in range(0,49,2):
        x,y=flight_route(k/48);d.point((round(x),round(y)),fill=(54,83,101))
    d.ellipse((3,18,24,39),fill=(169,66,85));d.ellipse((5,20,22,37),fill=(238,122,104))
    d.polygon([(-7,48),(14,24),(37,48)],fill=(72,98,141))
    d.polygon([(5,34),(14,24),(23,34),(19,32),(16,35),(13,32),(10,34),(8,32)],fill=(234,239,228))
    d.polygon([(14,24),(37,48),(24,48)],fill=(39,64,102))
    d.line((14,36,19,44),fill=(86,123,161))
    # Render the detailed station on its own layer, then give Japan equal space.
    station=Image.new('RGBA',(64,64));d=ImageDraw.Draw(station)
    stone=(182,139,91);light=(237,199,132);shade=(102,77,62);roof=(42,72,78)
    d.rectangle((11,33,63,48),fill=shade)
    d.rectangle((12,33,62,46),fill=stone)
    # Central dome silhouette and concentric copper ribs.
    d.ellipse((28,12,50,33),fill=(24,47,60))
    d.ellipse((29,13,49,31),fill=roof)
    d.arc((30,14,48,31),180,350,fill=(88,139,130))
    for rx in (3,6,9):d.arc((39-rx,13,39+rx,33),180,360,fill=(132,168,139))
    d.line((39,13,39,24),fill=(197,194,137))
    d.line((29,24,49,24),fill=(168,155,107))
    d.rectangle((30,25,48,29),fill=stone)
    for x in range(31,49,4):d.rectangle((x,25,x+1,28),fill=(61,72,68))
    d.line((30,29,48,29),fill=light)
    # Lantern and finial at the dome apex.
    d.line((39,7,39,10),fill=light)
    d.polygon([(36,12),(37,9),(41,9),(42,12)],fill=(106,148,126))
    d.rectangle((37,10,41,12),fill=light);d.point((39,10),fill=(52,87,91))
    # Matching small corner towers with stepped roofs and stone pilasters.
    for cx in (21,57):
        d.line((cx,21,cx,24),fill=light)
        d.polygon([(cx-5,28),(cx-3,25),(cx,23),(cx+3,25),(cx+5,28)],fill=roof)
        d.line([(cx-4,27),(cx,24),(cx+4,27)],fill=(122,163,139))
        d.rectangle((cx-4,29,cx+4,46),fill=stone)
        d.line((cx-5,29,cx+5,29),fill=light)
        for x in (cx-4,cx+4):
            d.line((x,31,x,45),fill=light)
            d.point((x,32),fill=(255,226,165))
        d.rectangle((cx-2,31,cx+2,35),fill=(33,58,70))
        d.arc((cx-2,30,cx+2,34),180,360,fill=light)
        d.line((cx,31,cx,35),fill=(197,156,99))
        d.rectangle((cx-2,39,cx+2,44),fill=(39,59,65))
        d.arc((cx-2,38,cx+2,42),180,360,fill=light)
        d.line((cx,39,cx,44),fill=(212,178,117))
    # Architectural courses and cornices across the wings.
    for y in (35,38,45):d.line((12,y,62,y),fill=(222,174,108))
    for x in (12,16,26,29,49,52,62):
        d.line((x,34,x,46),fill=(232,193,123))
    for x in (14,27,51):
        for y in (34,40):
            d.rectangle((x,y,x+1,y+3),fill=(40,57,65))
            d.point((x,y+1),fill=(212,169,88))
    # Central pediment and circular clock, shadowed carvings on each side.
    d.polygon([(28,33),(32,30),(35,27),(39,26),(43,27),(46,30),(50,33)],fill=light)
    d.line([(28,33),(35,28),(39,27),(43,28),(50,33)],fill=(250,219,154))
    d.ellipse((36,27,42,33),fill=(79,73,61))
    d.ellipse((37,28,41,32),fill=(254,229,160))
    a=-math.pi/2+TAU*t
    d.line((39,30,39+round(2*math.cos(a)),30+round(2*math.sin(a))),fill=(53,61,65))
    d.line((39,30,40,29),fill=(53,61,65))
    for x in (32,46):d.point((x,31),fill=(119,93,63))
    # Tall arched glazing: stone archivolt, three mullions, horizontal transoms.
    d.rectangle((30,34,48,46),fill=shade)
    d.ellipse((31,32,47,45),fill=light)
    d.rectangle((31,39,47,46),fill=light)
    d.ellipse((33,34,45,44),fill=(30,64,80))
    d.rectangle((33,40,45,46),fill=(30,64,80))
    for x in (35,39,43):d.line((x,36 if x==39 else 37,x,46),fill=(153,160,120))
    for y in (39,42):d.line((33,y,45,y),fill=(161,170,133))
    # Occasional warm panes, while keeping structural lines stationary.
    for k,(x,y) in enumerate([(34,40),(40,43),(44,40)]):
        c=(222,174,91) if math.sin(TAU*t+k)>.1 else (96,139,131)
        d.rectangle((x,y,x+1,y+1),fill=c)
    for x in (31,47):d.line((x,35,x,46),fill=(255,216,144))
    d.line((12,47,63,47),fill=light);d.line((10,48,63,48),fill=(123,102,79))
    station=station.crop((10,0,64,49)).resize((39,49),Image.Resampling.NEAREST)
    im.paste(station,(25,9),station);d=ImageDraw.Draw(im)
    # Rain-dark forecourt: broken reflections, converging paving joints, lamps.
    d.rectangle((0,55,63,63),fill=(9,23,36))
    for y in (55,57):
        for x in range(3,64,8):
            dx=round(math.sin(TAU*t+y+x)*1.5)
            d.line((x+dx,y,x+dx+3,y),fill=(68,68,56) if x>20 else (29,53,68))
    for x in range(0,65,12):d.line((45,55,x,58),fill=(25,39,49))
    for x in (11,61):
        d.line((x,44,x,51),fill=(42,50,53));d.point((x,44),fill=(255,228,157))
    # Large foreground torii: Japan now occupies almost half of the composition.
    d.rectangle((3,39,5,53),fill=(182,55,63));d.rectangle((19,39,21,53),fill=(182,55,63))
    d.line([(0,36),(5,38),(20,38),(24,36)],fill=(248,122,101),width=2)
    d.line((2,42,23,42),fill=(208,72,67),width=2)
    d.line((4,39,4,52),fill=(250,136,103));d.line((20,39,20,52),fill=(250,136,103))
    # Petals restricted to the Japan sky; continuous wrapped paths.
    for k in range(4):
        x=round((k*7+t*26)%28)-2;y=round(23+k*4+math.sin(TAU*t+k))
        d.point((x,y),fill=(246,161,181))
    # Equal 14x9 flags and mirrored flagpoles; no text anywhere in this work.
    d.line((3,14,3,30),fill=(146,160,164))
    fy=14+round(math.sin(TAU*t))
    d.rectangle((4,fy,17,fy+8),fill=(243,241,222))
    d.ellipse((8,fy+1,13,fy+6),fill=(212,45,64))
    d.line((62,14,62,30),fill=(146,160,164))
    d.rectangle((48,fy,52,fy+8),fill=(35,38,44))
    d.rectangle((53,fy,56,fy+8),fill=(250,199,54))
    d.rectangle((57,fy,61,fy+8),fill=(225,52,66))
    # Constant-speed crossing. Start and end entirely outside the canvas,
    # so neither disappearance on a building nor a visible loop teleport occurs.
    x,y,a,q=flight_pose(t)
    if -6<x<70:
        travel=Image.new('RGBA',(64,64));td=ImageDraw.Draw(travel)
        for k in range(49):
            p=k/48
            if max(0,q-.14)<p<q and k%2==0:
                px,py=flight_route(p);td.point((round(px),round(py)),fill=(146,205,218,255))
        # Analytic pitch, limited to 20 degrees, keeps the small silhouette readable.
        def aircraftpoint(px,py):return (round(x+px*math.cos(a)-py*math.sin(a)),round(y+px*math.sin(a)+py*math.cos(a)))
        td.polygon([aircraftpoint(px,py) for px,py in [(5,0),(1,1),(-1,3),(-2,3),(-1,1),(-4,1),(-5,2),(-5,-2),(-4,-1),(-1,-1),(-2,-3),(-1,-3),(1,-1)]],fill=(236,245,240,255))
        td.point(aircraftpoint(2,0),fill=(50,105,142,255))
        im=Image.alpha_composite(im.convert('RGBA'),travel).convert('RGB');d=ImageDraw.Draw(im)
    # Ocean and distant warm reflections reinforce the length of the journey.
    for k in range(4):
        x=3+k*16+round(math.sin(TAU*t+k)*2)
        d.line((x,59,x+7,59),fill=(27,67,89))
        d.line((x+3,62,x+7,62),fill=(18,45,67))
    return im

def java(t):
    im,d=base(t)
    # Perspective circuit board with flowing packets.
    for k in range(7):
        x=4+k*9
        d.line([(32,39),(x,52),(x,63)],fill=(22,60,70))
        phase=(t*2+k/7)%1
        y=43+round(phase*20);px=round(32+(x-32)*min(1,(y-39)/13))
        d.rectangle((px,y,px+1,y+1),fill=[(254,183,58),(245,66,77),(100,213,216)][k%3])
    d.ellipse((11,46,53,53),fill=(22,45,67));d.arc((11,45,53,52),0,180,fill=(89,174,181))
    bob=round(math.sin(TAU*t));y=29+bob
    # Steam braided into two animated streams; code glyphs rise from the cup.
    for k in range(2):
        points=[(round(27+k*10+3*math.sin(TAU*t+q*.4+k*2)),y-q) for q in range(3,18)]
        d.line(points,fill=(46,91,112),width=3)
        d.line(points,fill=(97,204,209))
    for k,s in enumerate(['{','}','</>']):
        phase=(t+k/3)%1;yy=round(y-5-phase*13)
        xx=round(23+k*5+2*math.sin(TAU*t+k))
        text(d,s,yy,(177,237,223),x=xx)
    d.ellipse((42,y+3,52,y+14),fill=(116,171,175))
    d.ellipse((44,y+5,49,y+11),fill=INK)
    d.rounded_rectangle((17,y,44,y+18),radius=5,fill=(164,210,206))
    d.rectangle((18,y+5,21,y+12),fill=(219,238,218))
    d.rectangle((36,y+5,43,y+12),fill=(86,150,162))
    d.ellipse((17,y-3,44,y+5),fill=(231,233,208))
    d.ellipse((20,y-1,41,y+3),fill=(73,37,37))
    d.arc((22,y,39,y+3),0,180,fill=(183,104,61))
    # Japanese and Belgian flag badges in the porcelain.
    d.rectangle((24,y+7,29,y+11),fill=(244,237,213));d.ellipse((26,y+8,28,y+10),fill=(217,65,73))
    for x,c in zip((32,34,36),[(20,24,31),(250,197,51),(233,64,75)]):d.rectangle((x,y+7,x+1,y+11),fill=c)
    text(d,'JAVA',1,(255,182,82),scale=2)
    text(d,'DEVOXX',57,(123,219,213))
    return im

def portal(t):
    im,d=base(t)
    # Orbital portal: rotating nine-sphere lattice in a neon torii frame.
    for r,c in [(23,(21,48,73)),(21,(41,100,120))]:d.ellipse((32-r,31-r,32+r,31+r),outline=c)
    for k in range(12):
        a=TAU*t+k*TAU/12
        x=32+round(23*math.cos(a));y=31+round(20*math.sin(a))
        sphere(d,x,y,1,[(249,193,56),(235,69,86),(109,226,214)][k%3])
    d.rectangle((9,17,11,52),fill=(159,47,70));d.rectangle((52,17,54,52),fill=(159,47,70))
    d.line([(6,13),(12,15),(51,15),(57,13)],fill=(255,114,105),width=2)
    d.line((8,20,55,20),fill=(213,68,86),width=2)
    pts=atomium(d,t,32,34,14,True)
    # A light packet walks the center-to-corner connections.
    k=int(t*8)%8;q=(t*8)%1
    x=32+(pts[k][0]-32)*q;y=34+(pts[k][1]-34)*q
    sphere(d,x,y,1,(255,208,84))
    # Perspective reflective floor.
    for y in [54,58,63]:d.line((0,y,63,y),fill=(23,56,74))
    for x in range(-16,81,16):d.line((32,49,x,63),fill=(23,56,74))
    text(d,'DEVOXX',2,(255,203,95),scale=2)
    text(d,'JAVA',56,(145,230,216))
    d.rectangle((2,57,9,61),fill=(235,230,211));d.ellipse((4,58,7,60),fill=(218,65,75))
    for x,c in zip((54,57,60),[(21,25,30),(249,196,48),(237,59,71)]):d.rectangle((x,57,x+2,61),fill=c)
    return im

WORKS=[('01-japan-belgium-express','Across the Seas — Japan to Antwerp',bridge),
       ('02-java-steam-to-code','Java — Steam to Code',java),
       ('03-devoxx-atomium-portal','Devoxx — Atomium Portal',portal)]

def main():
    for p in ['work/rgb','previews','submissions']: (ROOT/p).mkdir(parents=True,exist_ok=True)
    manifest=[]
    for name,title,fn in WORKS:
        frames=[fn(i/N) for i in range(N)]
        # One deterministic palette for the whole animation avoids color flicker.
        atlas=Image.new('RGB',(64,64*N))
        for i,f in enumerate(frames):atlas.paste(f,(0,i*64))
        palette=atlas.quantize(colors=128,method=Image.Quantize.MEDIANCUT)
        frames=[f.quantize(palette=palette,dither=Image.Dither.NONE).convert('RGB') for f in frames]
        (ROOT/'work/rgb'/f'{name}.rgb').write_bytes(b''.join(f.tobytes() for f in frames))
        preview=[f.resize((512,512),Image.Resampling.NEAREST) for f in frames]
        preview[0].save(ROOT/'previews'/f'{name}.gif',save_all=True,append_images=preview[1:],duration=DELAY,loop=0,optimize=False)
        frames[N//4].resize((512,512),Image.Resampling.NEAREST).save(ROOT/'previews'/f'{name}.png')
        manifest.append(dict(file=f'submissions/{name}.gif',title=title,size=[64,64],frames=N,delay_ms=DELAY,duration_ms=N*DELAY,palette_colors=128,encoder='Jixoo GifEncoder'))
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    sheet=Image.new('RGB',(3*512,512))
    for k,(name,_,_) in enumerate(WORKS):sheet.paste(Image.open(ROOT/'previews'/f'{name}.png'),(k*512,0))
    sheet.save(ROOT/'previews/contact-sheet.png')
    print('Generated three original 64x64 animations, 128 frames each.')

if __name__=='__main__':main()
