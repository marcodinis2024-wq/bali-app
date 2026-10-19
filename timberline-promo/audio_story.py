# Música e efeitos sonoros de "A porta está aberta" (50 s).
# Tudo sintetizado em código: piano, cordas sintetizadas, pulso de baixo e sons de foley.
import numpy as np, wave, os
from scipy.signal import butter, sosfilt, fftconvolve
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SR = 48000; DUR = 50.0; N = int(SR*DUR)
rng = np.random.default_rng(7)
def tt(d): return np.arange(int(d*SR))/SR
def mtof(m): return 440*2**((m-69)/12)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype='band', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype='high', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype='low', fs=SR, output='sos'), x)

class Bus:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)
    def add(s, x, t0, g=1.0, pan=0.0):
        i = int(round(t0*SR))
        if i < 0 or i >= N: return
        if x.ndim == 2: l, r = x[0], x[1]
        else:
            l = x*np.cos((pan+1)*np.pi/4)*1.414; r = x*np.sin((pan+1)*np.pi/4)*1.414
        n = min(len(l), N-i); s.L[i:i+n] += l[:n]*g; s.R[i:i+n] += r[:n]*g

# ── instrumentos ──
def piano(f, d=2.0, vel=1.0):
    t = tt(d); x = np.zeros(len(t))
    for k, a in enumerate([1, .5, .28, .14, .07], 1):
        x += a*np.sin(2*np.pi*f*k*(1+.0003*k*k)*t)*np.exp(-t*(1.3+.9*k))
    x += lp(rng.standard_normal(len(t)), 2500)*np.exp(-t*90)*.04
    return x*np.minimum(1, t/.004)*vel

def strings(freqs, d):
    t = tt(d); x = np.zeros(len(t))
    for f in freqs:
        for det in (-.12, 0, .12):
            ff = f*2**(det/12); x += np.sin(2*np.pi*ff*t + .8*np.sin(2*np.pi*.3*t))
    x = lp(x, 1800)/(len(freqs)*3)
    return x*np.minimum(1, t/1.2)*np.minimum(1, (d-t)/1.5)

def sub(f, d):
    t = tt(d); return np.sin(2*np.pi*f*t)*np.minimum(1, t/.02)*np.exp(-t*2.2)

def kick():
    t = tt(.4); f = 45 + 70*np.exp(-t*30)
    x = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)
    return np.tanh(x*1.6)

def bell(f, d=2.5):
    t = tt(d); x = np.zeros(len(t))
    for r, a, k in [(1, 1, 1.6), (2.0, .4, 3), (3.01, .25, 5), (4.2, .12, 8)]:
        x += a*np.sin(2*np.pi*f*r*t)*np.exp(-t*k)
    return x*np.minimum(1, t/.002)

# ── foley ──
def pencil(d=3.0):
    # grafite no papel: ruído bandpass modulado por micro-impactos
    t = tt(d); x = bp(rng.standard_normal(len(t)), 1800, 7000)
    x *= .35+.25*np.sin(2*np.pi*11*t)+.15*np.sin(2*np.pi*27*t+1)
    x *= np.clip(np.sin(np.pi*t/d)*2, 0, 1)
    return x/np.max(np.abs(x))*.7

def wind(d=10.0):
    t = tt(d); x = lp(rng.standard_normal(len(t)), 500, 2)
    x *= (.5+.5*np.sin(np.pi*t/d))*(.8+.2*np.sin(2*np.pi*.15*t))
    return x/np.max(np.abs(x))*.6

def birds(d=1.0, f0=2400):
    t = tt(d); f = f0*(1+.25*np.sin(2*np.pi*9*t))
    x = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*4)*np.minimum(1, t/.01)
    return x*.25

def knock():
    t = tt(.25)
    x = np.sin(2*np.pi*240*t)*np.exp(-t*30)+.5*np.sin(2*np.pi*640*t)*np.exp(-t*50)
    x += bp(rng.standard_normal(len(t)), 900, 4000)*np.exp(-t*120)*.6
    return x

def door(d=1.6):
    # rangido: frequência a subir e a descer com ruído de madeira
    t = tt(d); f = 180+120*np.sin(2*np.pi*.7*t)+60*t
    x = np.sin(2*np.pi*np.cumsum(f)/SR)*.25 + bp(rng.standard_normal(len(t)), 300, 1500)*.4
    return x*np.sin(np.pi*np.clip(t/d, 0, 1))**.7

def whoosh(d=.8, up=True, lo=250, hi=6000):
    t = tt(d); n = len(t); noise = rng.standard_normal(n); x = np.zeros(n)
    prog = t/d if up else 1-t/d
    c = np.log(lo)+(np.log(hi)-np.log(lo))*np.sin(prog*np.pi/2)
    for i in range(12):
        b0, b1 = np.geomspace(lo, hi, 13)[i], np.geomspace(lo, hi, 13)[i+1]
        x += bp(noise, b0, b1)*np.exp(-((c-np.log(np.sqrt(b0*b1)))**2)/(2*.45**2))
    x *= np.sin(np.pi*np.clip(t/d, 0, 1))**1.6
    x /= np.max(np.abs(x))+1e-9
    pan = np.linspace(-.7, .7, n) if up else np.linspace(.7, -.7, n)
    return np.stack([x*np.cos((pan+1)*np.pi/4)*1.414, x*np.sin((pan+1)*np.pi/4)*1.414])

def boom(d=2.2):
    t = tt(d); f = 32+40*np.exp(-t*7)
    x = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.2)
    return np.tanh((x+lp(rng.standard_normal(len(t)), 700)*np.exp(-t*9)*.7)*1.5)

def tick(f=2600):
    t = tt(.03); return np.sin(2*np.pi*f*t)*np.exp(-t*160)

def pop(f=880):
    t = tt(.12); ff = f*(1+.8*np.exp(-t*60))
    return np.sin(2*np.pi*np.cumsum(ff)/SR)*np.exp(-t*35)

def chime(d=1.8):
    return bell(1174, d)*.7+bell(1568, d)*.45

# ── música (Ré maior, 72 BPM, compasso de 3,33 s) ──
mus = Bus(); drm = Bus(); send = Bus()
BAR = 60/72*4
CH = [[62, 66, 69, 73, 76], [59, 62, 66, 69, 73], [55, 59, 62, 66, 69], [57, 61, 64, 67, 71]]  # Dmaj9 · Bm7 · G · A
ROOT = [38, 35, 31, 33]
def sec(t):
    if t < 4: return 'intro'
    if t < 9: return 'swell'
    if t < 17: return 'build'
    if t < 37: return 'main'
    if t < 44: return 'calm'
    return 'end'

bars = int(np.ceil(DUR/BAR))+1
for b in range(bars):
    t0 = b*BAR; c = CH[b % 4]; r = ROOT[b % 4]; s = sec(t0+.01)
    if t0 >= DUR: break
    mus.add(strings([mtof(n) for n in c[:4]], BAR+.5), t0, .32 if s in ('intro', 'calm') else .42)
    if s in ('build', 'main'):
        mus.add(sub(mtof(r), BAR*.95), t0, .6)
    if s in ('swell', 'build', 'main', 'calm'):
        seq = [0, 2, 3, 4, 2, 3, 1, 4] if s != 'calm' else [0, 4, 2, 4]
        step = BAR/8 if s != 'calm' else BAR/4
        for i, k in enumerate(seq):
            ts = t0+i*step
            if sec(ts) == 'end': continue
            mus.add(piano(mtof(c[k]+12), 2.2, .45+.25*(i % 2 == 0)), ts, .34, pan=-.25 if i % 2 else .25)
            send.add(piano(mtof(c[k]+12), 2.2, .3), ts, .24)

# pulso de baixo e kick
for b in range(bars):
    t0 = b*BAR
    if sec(t0+.01) in ('build', 'main'):
        for beat in (0, 2):
            drm.add(kick(), t0+beat*BAR/4, .75)
# melodia sparse
MEL = [(0, 74), (2, 78), (4, 81), (6, 79), (8, 78), (10, 74)]
for start in (20.0, 30.0):
    for pos, m in MEL:
        ts = start+pos*BAR/12
        mus.add(bell(mtof(m), 2.0), ts, .15, pan=.2); send.add(bell(mtof(m), 2.0), ts, .22)
mus.add(strings([mtof(n) for n in [62, 69, 74]], 6.0), 44.0, .3)
mus.add(strings([mtof(n) for n in [50, 62, 66, 69]], 6.0), 44.5, .45)
drm.add(kick(), 50.0-.6, .7)

# efeitos com ducking suave da música em volta dos impactos
tl = np.arange(N)/SR
env = np.ones(N)
for t_imp in [23.5, 36.0, 44.0]:
    env *= 1-.25*np.exp(-np.abs(tl-t_imp)*6)
mus.L *= env; mus.R *= env

fx = Bus()
# 1 gancho: grafite e respiração
fx.add(pencil(3.0), .15, .55)
fx.add(bell(2093, 1.2)*.06, 2.9, .4)
# 2 terreno: vento, pássaros, passo de madeira
fx.add(wind(10.0), 3.8, .42)
for i, t0 in enumerate([5.2, 5.5, 6.1, 6.4, 7.6, 7.9]): fx.add(birds(.35, 2400+i*180), t0, .18, pan=(i % 3-1)*.5)
# 3 fundação: batidas de madeira a cada pilar
r = np.random.default_rng(3)
for t0 in np.arange(9.7, 14.8, .32): fx.add(knock(), t0, .42, pan=r.uniform(-.5, .5))
fx.add(whoosh(.6, True), 9.0, .25)
fx.add(boom(1.4), 9.6, .45)
# 4 o que não se vê: cliques de luz
for i, t0 in enumerate([17.8, 18.5, 19.2, 19.9]): fx.add(tick(2200+i*200), t0, .22); fx.add(pop(700+i*90), t0+.02, .14)
fx.add(whoosh(.5, False), 17.2, .22)
# 5 a porta está aberta: rangido e impacto de luz
fx.add(door(1.6), 23.3, .5)
fx.add(pop(900), 23.6, .3)
fx.add(boom(1.8), 23.7, .65)
fx.add(chime(2.0), 25.8, .32)
fx.add(whoosh(.7, True, 500, 6000), 22.9, .22)
# 6 jantar: campainha e passos abafados
fx.add(chime(2.4), 30.4, .3)
for t0 in [31.0, 31.5]: fx.add(tick(1500), t0, .12)
fx.add(whoosh(.8, False), 36.0, .2)
# 7 como se começa: três passos
for i, t0 in enumerate([37.9, 38.7, 39.5]): fx.add(pop(780+i*120), t0, .34); fx.add(tick(2400), t0+.01, .15)
fx.add(whoosh(.5, True), 37.2, .2)
# 8 final: emblema, acorde e sino
fx.add(whoosh(.7, True, 300, 7000), 44.0, .25)
fx.add(chime(3.0), 45.6, .4)
fx.add(boom(2.4), 48.9, .32)

# mistura e espaço
ir_t = tt(2.0); ir = rng.standard_normal((2, len(ir_t)))*np.exp(-ir_t*2.8)
ir[:, :int(.02*SR)] *= np.linspace(0, 1, int(.02*SR))
rev = np.stack([fftconvolve(lp(hp(send.L, 200), 6000), ir[0])[:N], fftconvolve(lp(hp(send.R, 200), 6000), ir[1])[:N]])
rev /= np.max(np.abs(rev))+1e-9
music = np.stack([mus.L, mus.R])+np.stack([drm.L, drm.R]); music /= np.max(np.abs(music))+1e-9
sfx = np.stack([fx.L, fx.R]); sfx /= np.max(np.abs(sfx))+1e-9
out = music*.62+sfx*.7+rev*.14
fade = np.ones(N); fi = int(.05*SR); fade[:fi] = np.linspace(0, 1, fi)
f0 = int(48.8*SR); fade[f0:] = np.linspace(1, 0, N-f0)**1.5
out *= fade; out = np.tanh(out*1.2)/np.tanh(1.2); out /= np.max(np.abs(out))/.95
with wave.open('audio_story.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out.T*32767).astype(np.int16).tobytes())
print('ok')
