"""Make the illustrative uniform-star transit movie and a mid-transit poster.

The opaque planet has radius 0.1 stellar radii and crosses the stellar center
at constant projected speed. Animation time pauses at mid-transit; the plot's
horizontal coordinate is proportional to physical time during the motion.
"""
from math import acos, pi, sqrt
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parent / 'assets'
WIDTH, HEIGHT, FPS, DURATION = 1280, 720, 24, 12
RATIO = .1
NAVY = '#071e32'
INK = '#20394d'
TEAL = '#087e81'
GOLD = '#dba237'
WHITE = '#ffffff'

def occulted_fraction(distance, radius=RATIO):
    """Fraction of a unit-radius uniform stellar disk occulted by a disk."""
    d = abs(distance)
    if d >= 1 + radius:
        return 0.0
    if d <= 1 - radius:
        return radius * radius
    a = acos(max(-1., min(1., (d*d + 1 - radius*radius)/(2*d))))
    b = acos(max(-1., min(1., (d*d + radius*radius - 1)/(2*d*radius))))
    radicand = (-d + 1 + radius)*(d + 1 - radius)*(d - 1 + radius)*(d + 1 + radius)
    area = a + radius*radius*b - .5*sqrt(max(0., radicand))
    return area / pi

def position(t):
    if t < 5.0:
        return -1.3 + 1.3*t/5.0
    if t <= 7.0:
        return 0.0
    return 1.3*(t-7.0)/5.0

def font(size, bold=False):
    p = '/System/Library/Fonts/Helvetica.ttc'
    return ImageFont.truetype(p, size, index=1 if bold else 0)

def render(t, poster=False):
    im = Image.new('RGB', (WIDTH, HEIGHT), WHITE)
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle((20, 20, 610, 665), radius=16, fill=NAVY)
    dr.text((46, 43), 'A planet crosses its star', font=font(30, True), fill=WHITE)
    cx, cy, rs = 314, 360, 188
    # Plain uniform disk: no visual limb darkening.
    dr.ellipse((cx-rs,cy-rs,cx+rs,cy+rs), fill='#f5c65f', outline='#ffe8ad', width=3)
    x = position(t)
    px, py, rp = cx + x*rs, cy, rs*RATIO
    dr.ellipse((px-rp,py-rp,px+rp,py+rp), fill=NAVY, outline='#7fc1c3', width=2)
    dr.text((48, 607), 'Central transit', font=font(23), fill='#d6e8ee')
    dr.text((659, 45), 'The predicted light curve', font=font(30, True), fill=INK)
    left, right, top, bottom = 716, 1214, 158, 554
    dr.line((left,top,left,bottom,right,bottom), fill=INK, width=3)
    xmin, xmax, ymin, ymax = -1.3, 1.3, .984, 1.002
    sx = lambda v: left + (v-xmin)/(xmax-xmin)*(right-left)
    sy = lambda v: bottom - (v-ymin)/(ymax-ymin)*(bottom-top)
    for y in (.985, .990, .995, 1.000):
        yy = sy(y)
        dr.line((left,yy,right,yy), fill='#dbe5e8', width=1)
        dr.text((left-65,yy-12), f'{y:.3f}', font=font(19), fill=INK)
    for tick in (-1., 0., 1.):
        xx = sx(tick)
        dr.line((xx,bottom,xx,bottom+7), fill=INK, width=2)
        dr.text((xx-13,bottom+13), f'{tick:.0f}', font=font(20), fill=INK)
    points = 400
    plot_end = xmax if poster else x
    pts = []
    for i in range(points+1):
        u = xmin + (plot_end-xmin)*i/points
        pts.append((sx(u),sy(1-occulted_fraction(u))))
    if len(pts)>1:
        dr.line(pts, fill=TEAL, width=5, joint='curve')
    fx, fy = sx(x), sy(1-occulted_fraction(x))
    dr.ellipse((fx-7,fy-7,fx+7,fy+7), fill=GOLD, outline=WHITE, width=2)
    dr.text((left+95, 600), 'Transit time (arbitrary units)', font=font(22), fill=INK)
    dr.text((left, 106), 'Normalized stellar flux', font=font(22), fill=INK)
    dr.text((683, 652), 'Uniform star; opaque planet', font=font(19), fill=INK)
    return im

def main():
    ASSETS.mkdir(exist_ok=True)
    assert abs(occulted_fraction(0)-.01) < 1e-14
    assert abs(occulted_fraction(.9)-.01) < 1e-14
    assert occulted_fraction(1.1) == 0
    assert abs(occulted_fraction(1.0)-occulted_fraction(-1.0)) < 1e-14
    render(6, poster=True).save(ASSETS/'transit-poster.png')
    args = ['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo',
            '-pix_fmt','rgb24','-s',f'{WIDTH}x{HEIGHT}','-r',str(FPS),'-i','-',
            '-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p',
            '-movflags','+faststart',str(ASSETS/'transit-light-curve.mp4')]
    proc = subprocess.Popen(args, stdin=subprocess.PIPE)
    try:
        for i in range(FPS*DURATION):
            proc.stdin.write(render(i/FPS).tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError('ffmpeg failed')
    except BaseException:
        proc.kill(); proc.wait()
        raise
    print('Created 12 s video and mid-transit poster; central depth = 0.01')

if __name__ == '__main__':
    main()
