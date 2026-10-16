# Banda sonora original do anúncio Timberline: cinemática, 120 BPM, Ré menor.
# Os efeitos estão sincronizados com os tempos de ad.html.
import numpy as np, wave, os
from scipy.signal import butter, sosfilt, fftconvolve
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SR = 48000; DUR = 42.0; N = int(SR*DUR)
rng = np.random.default_rng(21)
BEAT = .5; S16 = BEAT/4
def mtof(m): return 440*2**((m-69)/12)
def tt(d): return np.arange(int(d*SR))/SR
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype='band', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype='high', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype='low', fs=SR, output='sos'), x)

class Bus:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)
    def add(s, x, t0, g=1.0, pan=0.0):
        i = int(round(t0*SR))
        if i >= N or i < 0: return
        if x.ndim == 2: l, r = x[0], x[1]
        else:
            l = x*np.cos((pan+1)*np.pi/4)*1.414; r = x*np.sin((pan+1)*np.pi/4)*1.414
        n = min(len(l), N-i); s.L[i:i+n] += l[:n]*g; s.R[i:i+n] += r[:n]*g

# ── instrumentos ──
def piano(f, d=1.6, vel=1.0):
    t = tt(d); x = np.zeros(len(t))
    for k, a in enumerate([1, .55, .3, .18, .1, .06], 1):
        fk = f*k*(1 + .0004*k*k)
        x += a*np.sin(2*np.pi*fk*t)*np.exp(-t*(1.6 + k*1.1))
    x += lp(rng.standard_normal(len(t)), 3000)*np.exp(-t*80)*.05
    return x*np.minimum(1, t/.003)*vel

def pad(freqs, d):
    t = tt(d); x = np.zeros(len(t))
    for f in freqs:
        for det in (-.08, 0, .08):
            ff = f*2**(det/12); x += np.sin(2*np.pi*ff*t + 1.5*np.sin(2*np.pi*ff*.5*t))
    x = lp(x, 1600)/(len(freqs)*3)
    return x*np.minimum(1, t/.6)*np.minimum(1, (d-t)/.6)

def sub(f, d):
    t = tt(d); return np.sin(2*np.pi*f*t)*np.minimum(1, t/.01)*np.exp(-t*1.2)*np.minimum(1, (d-t)/.05)

def kick():
    t = tt(.45); f = 40 + 75*np.exp(-t*30)
    x = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*5.5)
    x[:int(.003*SR)] += hp(rng.standard_normal(int(.003*SR)), 3000)*.3
    return np.tanh(x*1.8)

def rim():
    t = tt(.12)
    return (bp(rng.standard_normal(len(t)), 1500, 5000)*np.exp(-t*60)*.6 + np.sin(2*np.pi*820*t)*np.exp(-t*70)*.5)

def hat(a=1):
    t = tt(.05); return hp(rng.standard_normal(len(t)), 8000)*np.exp(-t*90)*a

def bell(f, d=1.4):
    t = tt(d); x = np.zeros(len(t))
    for r, a, k in [(1, 1, 2.5), (2.0, .4, 4), (3.01, .25, 6), (4.2, .12, 9)]:
        x += a*np.sin(2*np.pi*f*r*t)*np.exp(-t*k)
    return x*np.minimum(1, t/.002)

# ── efeitos ──
def whoosh(d=.6, up=True, lo=200, hi=6000):
    t = tt(d); n = len(t); noise = rng.standard_normal(n)
    bands = np.geomspace(lo, hi, 12); x = np.zeros(n)
    prog = t/d if up else 1 - t/d
    c = np.log(lo) + (np.log(hi)-np.log(lo))*np.sin(prog*np.pi/2)
    for i in range(len(bands)-1):
        b = bp(noise, bands[i], bands[i+1]); bc = np.log(np.sqrt(bands[i]*bands[i+1]))
        x += b*np.exp(-((c-bc)**2)/(2*.45**2))
    x *= np.sin(np.pi*np.clip(t/d, 0, 1))**1.6; x /= np.max(np.abs(x)) + 1e-9
    pan = np.linspace(-.7, .7, n) if up else np.linspace(.7, -.7, n)
    return np.stack([x*np.cos((pan+1)*np.pi/4)*1.414, x*np.sin((pan+1)*np.pi/4)*1.414])

def boom(d=2.0):
    t = tt(d); f = 30 + 45*np.exp(-t*7)
    x = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.2)
    n = lp(rng.standard_normal(len(t)), 700)*np.exp(-t*9)*.8
    return np.tanh((x+n)*1.5)

def knock(f=260):
    # madeira: ressonância curta + ataque seco
    t = tt(.22)
    x = np.sin(2*np.pi*f*t)*np.exp(-t*28) + .5*np.sin(2*np.pi*f*2.71*t)*np.exp(-t*45)
    x += bp(rng.standard_normal(len(t)), 800, 4000)*np.exp(-t*120)*.6
    return x

def slap():
    # painel OSB a encostar: thump + estalo
    t = tt(.35)
    x = lp(rng.standard_normal(len(t)), 600)*np.exp(-t*18) + np.sin(2*np.pi*95*t)*np.exp(-t*14)*.8
    x += bp(rng.standard_normal(len(t)), 2000, 6000)*np.exp(-t*90)*.4
    return np.tanh(x*1.3)

def nail():
    t = tt(.08)
    return bp(rng.standard_normal(len(t)), 2500, 9000)*np.exp(-t*120) + np.sin(2*np.pi*1400*t)*np.exp(-t*90)*.3

def hiss(d=1.2):
    t = tt(d); x = bp(rng.standard_normal(len(t)), 1500, 9000)
    x *= (np.sin(np.pi*np.clip(t/d, 0, 1))**.8)*(1 + .3*np.sin(2*np.pi*13*t))
    return x/np.max(np.abs(x))

def shimmer(d=.9, seed=0):
    r = np.random.default_rng(seed); out = np.zeros((2, int((d+1.2)*SR)))
    for k in range(10):
        f = r.uniform(2200, 5600); o = r.uniform(0, d); b = bell(f, .9)*.25; i = int(o*SR); p = r.uniform(-1, 1)
        out[0, i:i+len(b)] += b*np.cos((p+1)*np.pi/4)*1.4; out[1, i:i+len(b)] += b*np.sin((p+1)*np.pi/4)*1.4
    return out

def tick(f=2400):
    t = tt(.03); return np.sin(2*np.pi*f*t)*np.exp(-t*160)

def pop(f=900):
    t = tt(.12); ff = f*(1 + .8*np.exp(-t*60))
    return np.sin(2*np.pi*np.cumsum(ff)/SR)*np.exp(-t*35)

def swish(d=.7):
    t = tt(d); x = bp(rng.standard_normal(len(t)), 600, 3500)
    return x*np.sin(np.pi*np.clip(t/d, 0, 1))**2*.8

def air(d=2.5):
    t = tt(d); x = bp(rng.standard_normal(len(t)), 300, 2500)
    x *= (np.sin(np.pi*np.clip(t/d, 0, 1)))*(0.6 + .4*np.sin(2*np.pi*.8*t))
    return x/np.max(np.abs(x))

def click():
    t = tt(.05); return hp(rng.standard_normal(len(t)), 2000)*np.exp(-t*200) + np.sin(2*np.pi*1100*t)*np.exp(-t*120)*.4

def riser(d=1.5):
    t = tt(d); x = whoosh(d, True, 300, 9000)[0]*(t/d)**1.6
    f = 150 + 900*(t/d)**2; x += .3*np.sin(2*np.pi*np.cumsum(f)/SR)*(t/d)**2
    return x

# ── música ──
mus = Bus(); drm = Bus(); send = Bus()
CH = [[50, 57, 60, 65, 69], [46, 53, 58, 62, 65], [41, 53, 57, 60, 64], [48, 55, 60, 64, 67]]  # Dm9 · Bb · F · C
ROOT = [38, 34, 41, 36]
def sec(t):
    if t < 2: return 'intro'
    if t < 8: return 'half'
    if t < 27.5: return 'full'
    if t < 28: return 'break'
    if t < 32: return 'reveal'
    if t < 35.5: return 'full'
    if t < 36: return 'break'
    if t < 40: return 'full'
    return 'end'

for bar in range(21):
    t0 = bar*2.0; c = CH[bar % 4]; r = ROOT[bar % 4]; s = sec(t0 + .01)
    if s == 'end': continue
    mus.add(pad([mtof(n) for n in c[:4]], 2.1), t0, .5 if s in ('reveal',) else .32)
    if s != 'intro':
        mus.add(sub(mtof(r), 1.9), t0, .55 if s != 'reveal' else .35)
    # arpejo de piano em colcheias
    if s in ('half', 'full', 'reveal'):
        seq = [0, 2, 3, 4, 3, 2, 1, 3] if s != 'reveal' else [0, 4, 3, 2]
        step = .25 if s != 'reveal' else .5
        for i, k in enumerate(seq):
            ts = t0 + i*step
            if sec(ts) not in ('half', 'full', 'reveal'): continue
            x = piano(mtof(c[k] + 12), 1.2, .55 if i % 2 else .75)
            mus.add(x, ts, .32, pan=-.3 if i % 2 else .3); send.add(x, ts, .25)
    if s == 'reveal':
        x = sum(piano(mtof(n), 3.0, .6) for n in c); mus.add(x, t0, .22); send.add(x, t0, .3)

# melodia de sino (mais esparsa, premium)
MEL = [(0, 74), (3, 77), (6, 76), (8, 72), (12, 74), (14, 69)]
for start in (12.0, 20.0, 28.0, 36.0):
    for pos, m in MEL:
        ts = start + pos*.5
        x = bell(mtof(m), 1.6); mus.add(x, ts, .14, pan=.2); send.add(x, ts, .25)

t = 0.0
while t < 40.0:
    s = sec(t); b = round(t/BEAT)
    if s == 'half' and b % 2 == 0: drm.add(kick(), t, .9)
    if s == 'full':
        drm.add(kick(), t, .95)
        if b % 2 == 1: drm.add(rim(), t, .35, pan=.1)
        for k in range(2 if t < 18 else 4):
            drm.add(hat(1 if k % 2 else .6), t + k*(BEAT/(2 if t < 18 else 4)), .12, pan=.35)
    t += BEAT

fin = sum(piano(mtof(n), 2.0, .8) for n in [38, 50, 57, 60, 65, 69, 74])
mus.add(fin, 40.0, .3); send.add(fin, 40.0, .4); mus.add(pad([mtof(n) for n in [50, 57, 60, 65]], 2.0), 40.0, .45)
drm.add(kick(), 40.0, 1.0)

tl = np.arange(N)/SR
full = np.array([sec(x) == 'full' for x in np.floor(tl/BEAT)*BEAT])
sc = np.where(full, 1 - .4*np.exp(-(tl % BEAT)*9), 1.0)
mus.L *= sc; mus.R *= sc
# drone de abertura
d0 = pad([mtof(38), mtof(45), mtof(50)], 2.2); mus.add(d0, 0, .5)

# ── efeitos sincronizados ──
fx = Bus()
def W(t0, d=.6, g=.45, up=True): fx.add(whoosh(d, up), t0 - d*.45, g); send.add(whoosh(d, up)[0], t0 - d*.45, g*.25)
W(.2, .7, .35); fx.add(riser(1.6), .4, .2)
for i in range(6): fx.add(tick(1600 + i*90), .35 + i*.1, .25)
fx.add(boom(), 2.0, .9); fx.add(shimmer(.5, 1), 2.05, .4)
fx.add(shimmer(.6, 2), 2.6, .3)
W(3.85, .6, .45)
fx.add(shimmer(1.0, 3), 4.05, .4); W(4.7, .7, .3, False)
for i in range(8): fx.add(tick(2000 + i*60), 5.5 + i*.07, .15)
fx.add(swish(1.4), 6.0, .3); fx.add(tick(2600), 7.0, .25)
W(7.75, .6, .45)
T0, DT = 8.0, 3.3
st = lambda k: T0 + k*DT
for k in range(6):
    fx.add(tick(1800), st(k), .3); fx.add(swish(.5), st(k) - .1, .25)
    chips = 2 if k != 2 else 1
    for j in range(chips): fx.add(pop(900 + j*150), st(k) + .9 + j*.15, .3)
# 01 fundação
fx.add(slap(), st(0) + .25, .45); fx.add(boom(1.0), st(0) + .8, .5)
# 02 estrutura — pregar as vigas
r = np.random.default_rng(4)
for i in range(10): fx.add(knock(r.uniform(220, 320)), st(1) + .1 + i*.09, .35, pan=r.uniform(-.6, .6))
for i in range(12): fx.add(knock(r.uniform(240, 340)), st(1) + .4 + i*.085, .35, pan=r.uniform(-.6, .6))
fx.add(slap(), st(1) + 1.45, .35)
for i in range(12): fx.add(knock(r.uniform(260, 380)), st(1) + 1.5 + i*.085, .33, pan=r.uniform(-.6, .6))
fx.add(slap(), st(1) + 2.65, .35)
# 03 contraventamento — painéis + pregos
for o in [0, .35, .7, 1.1, 1.45, 1.8]:
    fx.add(slap(), st(2) + .3 + o, .5)
    for j in range(3): fx.add(nail(), st(2) + .45 + o + j*.06, .22)
# 04 isolamento — fusão térmica + vidro
for o in [0, .35, .7, 1.1, 1.45, 1.8]: fx.add(swish(.6), st(3) + .15 + o*.6, .25)
fx.add(hiss(1.2), st(3) + 1.0, .25); fx.add(hiss(1.2), st(3) + 1.5, .2)
for i in range(4): fx.add(shimmer(.3, 10 + i), st(3) + 1.6 + i*.15, .22)
# 05 fachada — barramento
for o in [0, .35, .7, 1.1, 1.45, 1.8]: fx.add(swish(.8), st(4) + .15 + o*.5, .25)
fx.add(slap(), st(4) + 1.5, .3)
# 06 conforto — luzes + ar
for i in range(4): fx.add(click(), st(5) + .3 + i*.12, .35); fx.add(bell(1046 + i*196, .8), st(5) + .32 + i*.12, .08)
fx.add(air(2.6), st(5) + .6, .18)
# revelação
fx.add(riser(1.0), 27.0, .3); fx.add(boom(2.2), 28.0, .8); fx.add(click(), 28.1, .5); fx.add(shimmer(1.0, 20), 28.15, .35)
fx.add(pop(800), 29.9, .3); fx.add(pop(950), 30.1, .3)
W(31.95, .6, .45)
for i in range(4):
    t0 = 32.75 + i*.55; fx.add(whoosh(.35, True, 500, 5000), t0 - .1, .2); fx.add(swish(.4), t0 + .35, .18)
W(35.75, .55, .45); fx.add(riser(.8), 35.2, .22)
fx.add(boom(), 36.0, .8)
for i in range(3): fx.add(pop(700 + i*120), 36.45 + i*.2, .3)
W(38.45, .6, .45); fx.add(shimmer(1.0, 30), 38.65, .35)
fx.add(boom(2.0), 40.0, .5); fx.add(pop(800), 40.05, .3)
for i in range(3): fx.add(tick(2200 + i*120), 40.3 + i*.1, .2)

# ── mistura ──
ir_t = tt(1.8); ir = rng.standard_normal((2, len(ir_t)))*np.exp(-ir_t*3.2)
ir[:, :int(.015*SR)] *= np.linspace(0, 1, int(.015*SR))
rev = np.stack([fftconvolve(lp(hp(send.L, 200), 6000), ir[0])[:N], fftconvolve(lp(hp(send.R, 200), 6000), ir[1])[:N]])
rev /= np.max(np.abs(rev)) + 1e-9
music = np.stack([mus.L, mus.R]) + np.stack([drm.L, drm.R]); music /= np.max(np.abs(music)) + 1e-9
sfx = np.stack([fx.L, fx.R]); sfx /= np.max(np.abs(sfx)) + 1e-9
out = music*.7 + sfx*.6 + rev*.16
fade = np.ones(N); fi = int(.05*SR); fade[:fi] = np.linspace(0, 1, fi)
f0 = int(41.2*SR); fade[f0:] = np.linspace(1, 0, N-f0)**1.5
out *= fade; out = np.tanh(out*1.2)/np.tanh(1.2); out /= np.max(np.abs(out))/.95
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out.T*32767).astype(np.int16).tobytes())
print('ok')
