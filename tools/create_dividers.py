"""Regenerate the small vector-style GIF dividers. Requires Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
S = 2
W = 1000
NAVY = '#10172F'
PLUM = '#59234F'
BLUE = '#315DA9'
IVORY = '#EEE5CC'
PINK = '#BD899C'
FONT = '/usr/share/fonts/opentype/urw-base35/URWBookman-LightItalic.otf'
SMALL = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'

def make(name, title=None, number=None, offset=0):
    height = 108 if title else 60
    frames = []
    for frame in range(64):
        t = 2 * math.pi * frame / 64
        im = Image.new('RGB', (W*S, height*S), NAVY)
        d = ImageDraw.Draw(im)
        def line(points, color, width=1):
            d.line([(int(x*S), int(y*S)) for x,y in points], fill=color, width=max(1,int(width*S)))
        def ellipse(x,y,r,fill,outline=None):
            d.ellipse(((x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S), fill=fill, outline=outline, width=2*S)
        def star(x,y,r,angle=0,fill=IVORY):
            pts=[]
            for j in range(10):
                a=angle-math.pi/2+j*math.pi/5
                rr=r*(1 if j%2==0 else .43)
                pts.append(((x+rr*math.cos(a))*S,(y+rr*math.sin(a))*S))
            d.polygon(pts,fill=fill)
        ybase = 82 if title else 30
        # A permanent stitched path; a short blue thread travels along it.
        def yy(x):
            return ybase + 3*math.sin(x/68 + offset)
        for x in range(26,974,12):
            line([(x,yy(x)),(x+6,yy(x+6))], '#8B8295', .8)
        center = 35 + (W-70) * (1-math.cos(t))/2
        for x in range(max(26,int(center-24)), min(974,int(center+24))):
            line([(x,yy(x)),(x+1,yy(x+1))],BLUE,2)
        if title:
            font=ImageFont.truetype(FONT,40*S)
            small=ImageFont.truetype(SMALL,12*S)
            d.text((26*S,29*S),number,font=small,fill=PINK)
            d.text((66*S,14*S),title,font=font,fill=IVORY)
            # A button rocks gently while the heading remains still.
            bx,by=918,43
            ellipse(bx,by,22,PLUM)
            ellipse(bx,by,17,IVORY)
            rot=.15*math.sin(t+offset)
            holes=[]
            for hx,hy in [(-5,-5),(5,-5),(-5,5),(5,5)]:
                x=bx+hx*math.cos(rot)-hy*math.sin(rot)
                y=by+hx*math.sin(rot)+hy*math.cos(rot)
                holes.append((x,y)); ellipse(x,y,2.3,NAVY)
            line([holes[0],holes[3]],BLUE,1.6)
            line([holes[1],holes[2]],BLUE,1.6)
            star(866,40+2*math.sin(t),8,.1*math.sin(t))
            star(963,48-2*math.sin(t),5,-.1)
        else:
            for i,x in enumerate([453,500,547]):
                ellipse(x,30,15,NAVY)
                star(x,30+1.5*math.sin(t+i),10 if i==1 else 6,.1*math.sin(t+i),IVORY if i==1 else PINK)
        frames.append(im.resize((W,height),Image.Resampling.LANCZOS))
    palette = frames[0].quantize(colors=96)
    frames = [f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    frames[0].save(OUT/name,save_all=True,append_images=frames[1:],duration=80,loop=0,optimize=True,disposal=1)
    print(name, (OUT/name).stat().st_size)

if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    make('agents-divider.gif','Building with agents','01')
    make('engineering-divider.gif','The engineering underneath','02',1)
    make('thread-divider.gif',offset=2)
