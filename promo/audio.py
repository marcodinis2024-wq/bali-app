import numpy as np, wave
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
DUR = 42.0
N = int(SR * DUR)
rng = np.random.default_rng(11)
BEAT = 0.5
S16 = BEAT / 4

def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)
def tt(d): return np.arange(int(d * SR)) / SR

class Bus:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)
    def add(s, x, t0, gain=1.0, pan=0.0):
        i = int(round(t0 * SR))
        if i >= N: return
        if x.ndim == 2: l, r = x[0], x[1]
        else:
            gl = np.cos((pan + 1) * np.pi / 4); gr = np.sin((pan + 1) * np.pi / 4)
            l, r = x * gl * 1.414, x * gr * 1.414
        n = min(len(l), N - i)
        if i < 0: return
        s.L[i:i+n] += l[:n] * gain; s.R[i:i+n] += r[:n] * gain

def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype='band', fs=SR, output='sos'), x)
def hp(x, f, order=2): return sosfilt(butter(order, f, btype='high', fs=SR, output='sos'), x)
def lp(x, f, order=2): return sosfilt(butter(order, f, btype='low', fs=SR, output='sos'), x)

# ───────── instruments ─────────
def marimba(f, d=0.45):
    t = tt(d)
    a = np.minimum(1, t / 0.002)
    return a * (np.sin(2*np.pi*f*t) * np.exp(-t*8) + .28*np.sin(2*np.pi*4*f*t) * np.exp(-t*28)
                + .08*np.sin(2*np.pi*9.9*f*t) * np.exp(-t*60))

def steelpan(f, d=0.9):
    t = tt(d)
    a = np.minimum(1, t / 0.004)
    mod = 1.3 * np.exp(-t*5) * np.sin(2*np.pi*2*f*t)
    x = np.sin(2*np.pi*f*t + mod) * np.exp(-t*3.2) + .25*np.sin(2*np.pi*3.01*f*t)*np.exp(-t*7)
    return a * x

def kick():
    t = tt(0.4)
    f = 42 + 90*np.exp(-t*28)
    ph = 2*np.pi*np.cumsum(f)/SR
    x = np.sin(ph) * np.exp(-t*6.5)
    x[:int(.004*SR)] += hp(rng.standard_normal(int(.004*SR)), 3000) * .4
    return np.tanh(x*1.6)

def clap():
    t = tt(0.25); x = np.zeros(len(t))
    for k, o in enumerate([0, .011, .022]):
        i = int(o*SR); n = len(t) - i
        x[i:] += rng.standard_normal(n) * np.exp(-t[:n]*(60 if k < 2 else 16))
    return bp(x, 900, 3200) * .9

def shaker(acc=1.0):
    t = tt(0.06)
    return hp(rng.standard_normal(len(t)), 6500) * np.exp(-t*70) * acc

def bass(f, d=0.3):
    t = tt(d)
    a = np.minimum(1, t/0.006) * np.exp(-t*3)
    rel = np.minimum(1, (d - t)/0.03)
    x = np.sin(2*np.pi*f*t) + .35*np.sin(2*np.pi*2*f*t) + .1*np.sin(2*np.pi*3*f*t)
    return np.tanh(x*1.4) * a * rel

def pad(freqs, d):
    t = tt(d); x = np.zeros(len(t))
    for f in freqs:
        for det in (-0.12, 0.0, 0.12):
            ff = f * 2**(det/12)
            x += 2*((t*ff) % 1) - 1
    x = lp(x, 1400) / (len(freqs)*3)
    env = np.minimum(1, t/0.25) * np.minimum(1, (d - t)/0.3)
    return x * env

# ───────── sfx ─────────
def whoosh(d=0.6, up=True, lo=250, hi=7000):
    t = tt(d); n = len(t)
    noise = rng.standard_normal(n)
    bands = np.geomspace(lo, hi, 14)
    x = np.zeros(n)
    prog = t/d if up else 1 - t/d
    centre = np.log(lo) + (np.log(hi)-np.log(lo)) * (np.sin(prog*np.pi/2)**1.2)
    for i in range(len(bands)-1):
        b = bp(noise, bands[i], bands[i+1])
        bc = np.log(np.sqrt(bands[i]*bands[i+1]))
        w = np.exp(-((centre - bc)**2) / (2*0.45**2))
        x += b * w
    env = np.sin(np.pi * np.clip(t/d, 0, 1))**1.6
    x = x * env
    x /= np.max(np.abs(x)) + 1e-9
    pan = np.linspace(-.8, .8, n) if up else np.linspace(.8, -.8, n)
    gl = np.cos((pan+1)*np.pi/4)*1.414; gr = np.sin((pan+1)*np.pi/4)*1.414
    return np.stack([x*gl, x*gr])

def pop(f0=650, d=0.16):
    t = tt(d)
    f = f0*(1 + 1.2*np.exp(-t*60))
    ph = 2*np.pi*np.cumsum(f)/SR
    x = np.sin(ph) * np.exp(-t*28)
    x[:int(.002*SR)] += rng.standard_normal(int(.002*SR))*.3
    return x

def tap():
    t = tt(0.06)
    x = hp(rng.standard_normal(len(t)), 2500)*np.exp(-t*220)*.6 + np.sin(2*np.pi*1900*t)*np.exp(-t*90)*.5
    return x

def key():
    t = tt(0.05)
    return hp(rng.standard_normal(len(t)), 1800)*np.exp(-t*260)*.8 + np.sin(2*np.pi*3100*t)*np.exp(-t*150)*.25

def bell(f=1320, d=1.2):
    t = tt(d); x = np.zeros(len(t))
    for r, a, k in [(1, 1, 3), (2.76, .45, 6), (5.4, .25, 9), (8.93, .12, 14)]:
        x += a*np.sin(2*np.pi*f*r*t)*np.exp(-t*k)
    return x * np.minimum(1, t/0.002)

def kaching():
    t = tt(1.3)
    ka = bp(rng.standard_normal(int(.07*SR)), 2500, 9000) * np.exp(-tt(.07)*50)
    x = np.zeros(len(t)); x[:len(ka)] += ka*1.2
    b = bell(1568, 1.2)*.6; i = int(.05*SR); x[i:i+len(b)] += b[:len(x)-i]
    b = bell(2093, 1.2)*.5; i = int(.11*SR); x[i:i+len(b)] += b[:len(x)-i]
    sh = hp(rng.standard_normal(len(t)), 7000)*np.exp(-t*5)*.15
    return x + sh

def boom(d=1.6):
    t = tt(d)
    f = 34 + 50*np.exp(-t*9)
    ph = 2*np.pi*np.cumsum(f)/SR
    x = np.sin(ph)*np.exp(-t*2.6)
    n = lp(rng.standard_normal(len(t)), 900)*np.exp(-t*10)*.9
    return np.tanh((x + n)*1.5)

def riser(d=1.5):
    t = tt(d)
    x = whoosh(d, True, 300, 9000)[0] * (t/d)**1.5
    f = 180 + 1100*(t/d)**2
    x += .25*np.sin(2*np.pi*np.cumsum(f)/SR)*(t/d)**2
    return x

def sparkle(n=9, d=0.6, seed=0):
    r = np.random.default_rng(seed)
    out = np.zeros((2, int((d+.4)*SR)))
    for k in range(n):
        f = r.uniform(2400, 5200); o = r.uniform(0, d)
        b = bell(f, .35)*.35
        i = int(o*SR); p = r.uniform(-1, 1)
        out[0, i:i+len(b)] += b*np.cos((p+1)*np.pi/4)*1.4
        out[1, i:i+len(b)] += b*np.sin((p+1)*np.pi/4)*1.4
    return out

def tick(i=0):
    t = tt(0.035)
    return np.sin(2*np.pi*(1800+i*25)*t)*np.exp(-t*140)

# ───────── music ─────────
mus = Bus(); drums = Bus(); send = Bus()
CH = [[55,59,62,67],[54,57,62,66],[55,59,64,67],[55,60,64,67]]
ROOT = [43,38,40,36]
NBARS = 21

def section(t):
    """0 intro, 1 full, 2 break, 3 end"""
    if t < 2.0: return 0
    if 27.5 <= t < 28.0 or 35.5 <= t < 36.0: return 2
    if t >= 40.0: return 3
    return 1

# marimba pattern (16th steps) + chord-tone index
MPAT = [(0,0),(3,1),(6,2),(8,3),(10,2),(12,1),(14,3)]
BPAT = [(0,0,3),(3,12,2),(6,0,2),(8,0,3),(11,12,2),(14,0,2)]  # step, octave, len(16ths)
for bar in range(NBARS):
    t0 = bar*2.0
    c = CH[bar % 4]; r = ROOT[bar % 4]
    for step, ci in MPAT:
        ts = t0 + step*S16; sec = section(ts)
        if sec == 3: continue
        g = .20 if sec == 0 else .26
        if sec == 2: g = .16
        note = c[ci] + 12
        x = marimba(mtof(note))
        mus.add(x, ts, g, pan=-.35 if ci % 2 else .35); send.add(x, ts, g*.5)
    if section(t0 + .01) in (1,) or (bar*2 >= 2 and section(t0) != 3):
        for step, octv, ln in BPAT:
            ts = t0 + step*S16
            if section(ts) != 1: continue
            mus.add(bass(mtof(r + octv), ln*S16*.95), ts, .42)
        mus.add(pad([mtof(n) for n in c], 2.0), t0, .30 if section(t0) == 1 else .18)
    elif section(t0) == 0:
        mus.add(pad([mtof(n) for n in c], 2.0), t0, .18)

# drums
t = 0.0
while t < 40.0:
    sec = section(t)
    b = round(t / BEAT)
    if sec == 1:
        drums.add(kick(), t, .95)
        if b % 2 == 1: drums.add(clap(), t, .42, pan=.05); send.add(clap(), t, .15)
    for k in range(4):
        ts = t + k*S16
        if section(ts) == 1:
            drums.add(shaker(1.0 if k == 2 else .5), ts, .16, pan=.3)
    t += BEAT

# melody (steel pan)
MEL = [(0,71),(2,74),(3,79),(5,76),(6,74),(8,69),(10,74),(11,78),(13,76),(14,74),
       (16,67),(18,71),(19,76),(21,74),(22,71),(24,72),(26,76),(27,79),(29,81),(30,79)]
for start in (4.0, 20.0, 28.0):
    for pos, m in MEL:
        ts = start + pos*0.25
        if section(ts) != 1: continue
        x = steelpan(mtof(m))
        mus.add(x, ts, .22, pan=.15); send.add(x, ts, .18)
# ending melody 36–40 first half + final
for pos, m in MEL[:10]:
    ts = 36.0 + pos*0.25
    x = steelpan(mtof(m)); mus.add(x, ts, .22, pan=.15); send.add(x, ts, .18)

# final hit at 40
fin = np.zeros(int(2.0*SR))
for n in [43, 55, 59, 62, 67, 71, 74, 79]:
    fin[:] += marimba(mtof(n), 2.0)*.18 + steelpan(mtof(n), 2.0)*.05
mus.add(fin, 40.0, 1.0); send.add(fin, 40.0, .6)
mus.add(pad([mtof(n) for n in [55,59,62,67]], 2.0), 40.0, .3)
drums.add(kick(), 40.0, 1.0)

# sidechain on music bus
tl = np.arange(N)/SR
sc = np.ones(N)
full = np.array([section(x) == 1 for x in (np.floor(tl/BEAT)*BEAT)])
ph = (tl % BEAT)
sc = np.where(full, 1 - .5*np.exp(-ph*9), 1.0)
mus.L *= sc; mus.R *= sc

# ───────── sfx cues ─────────
fx = Bus()
def W(t0, d=.6, g=.5, up=True): fx.add(whoosh(d, up), t0 - d*.45, g); send.add(whoosh(d, up)[0], t0 - d*.45, g*.3)
def POP(t0, f=650, g=.5, pan=0): fx.add(pop(f), t0, g, pan); send.add(pop(f), t0, g*.3)

W(0.25, .7, .45)
POP(.45, 420, .75); fx.add(boom(.9), .45, .35)
for i in range(6): POP(1.0 + i*.125, 560 + i*70, .42, pan=[-.6,.6,-.7,.7,-.4,.4][i])
W(1.95, .5, .55)
fx.add(riser(1.0), 1.0, .22)
fx.add(boom(), 2.0, .85); fx.add(sparkle(10, .5, 1), 2.1, .5)
fx.add(sparkle(8, .6, 2), 2.6, .35)
W(3.8, .6, .6)
W(4.4, .6, .45, False)
for i, t0 in enumerate([4.9, 5.25, 5.6, 5.95]): POP(t0, 700 + i*60, .42, pan=[.5,-.3,.6,-.4][i])
fx.add(whoosh(.9, False, 200, 3000), 5.3, .12)
W(7.8, .55, .5)
for i in range(26):
    tt0 = 8.15 + 1.2 * (1 - (1 - (i/25))**(1/3)) if False else 8.15 + 1.2*(1 - (1 - i/26)**0.5)
    fx.add(tick(i), tt0, .22)
fx.add(bell(1760, 1.0), 9.35, .3); POP(9.35, 500, .5)
for i in range(16):
    if i % 2 == 0: POP(9.55 + i*.1, 800 + (i % 5)*80, .28, pan=(i % 3 - 1)*.6)
W(11.75, .6, .5)
W(12.0, .5, .35, False)
POP(12.3, 600, .5); fx.add(tap(), 12.5, .5); fx.add(tap(), 13.35, .5)
POP(13.2, 680, .5)
for i in range(4): POP(13.35 + i*.12, 900 + i*90, .26)
for i, t0 in enumerate([13.85, 14.05, 14.25, 14.45, 14.65]): fx.add(key(), t0, .5, pan=.2)
POP(14.8, 760, .5); fx.add(sparkle(6, .4, 3), 14.9, .3)
W(15.95, .6, .55)
fx.add(tap(), 16.6, .5); fx.add(whoosh(.35, True, 400, 5000), 16.72, .3)
POP(16.9, 520, .45); fx.add(sparkle(6, .4, 4), 17.0, .3); POP(17.0, 820, .4)
fx.add(tap(), 17.75, .5); POP(17.85, 980, .45)
W(19.95, .55, .5)
fx.add(tap(), 20.15, .5); fx.add(kaching(), 20.3, .55)
for i, t0 in enumerate([20.65, 21.15, 21.65]): fx.add(whoosh(.35, True, 600, 6000), t0 - .1, .2); POP(t0 + .4, 700 + i*120, .45)
fx.add(sparkle(14, .8, 5), 22.6, .5); POP(22.6, 520, .55); fx.add(boom(.8), 22.6, .25)
W(23.9, .55, .5)
POP(24.3, 600, .45)
for i, t0 in enumerate([24.9, 25.4, 25.9]): POP(t0, 760 + i*110, .45); fx.add(tap(), t0 + .05, .2)
for i in range(16): fx.add(tick(i), 26.05 + .8*(1 - (1 - i/16)**0.6), .2)
fx.add(bell(1568, 1.2), 26.85, .32)
fx.add(tap(), 27.15, .5); fx.add(riser(.6), 27.3, .25)
W(27.5, .5, .45)
fx.add(whoosh(.7, True, 300, 8000), 28.3, .5)
fx.add(bell(1760, .9), 29.4, .28); fx.add(bell(2349, .9), 29.47, .22)
fx.add(boom(.8), 30.4, .35); POP(30.4, 540, .5); fx.add(sparkle(8, .5, 6), 30.45, .35)
W(31.9, .6, .55)
for i, t0 in enumerate([32.5, 33.0, 33.5, 34.0, 34.5]): POP(t0, 640 + i*80, .45, pan=[0,-.6,.6,-.6,.6][i])
fx.add(sparkle(8, .5, 7), 34.9, .3)
fx.add(riser(.9), 35.1, .28); W(35.75, .55, .5, False)
fx.add(boom(2.0), 36.05, .9); fx.add(sparkle(12, .6, 8), 36.1, .45)
fx.add(sparkle(8, .5, 9), 36.6, .3)
POP(37.3, 620, .5)
for i in range(6): POP(38.2 + i*.1, 700 + i*90, .3, pan=[-.6,.6,-.7,.7,-.4,.4][i])
fx.add(boom(2.0), 40.0, .5); fx.add(bell(1568, 2.0), 40.0, .3); fx.add(sparkle(10, .8, 10), 40.05, .35)

# ───────── mix ─────────
ir_t = tt(1.4)
ir = rng.standard_normal((2, len(ir_t))) * np.exp(-ir_t*4.2)
ir[:, :int(.01*SR)] *= np.linspace(0, 1, int(.01*SR))
revL = fftconvolve(lp(hp(send.L, 250), 7000), ir[0])[:N]
revR = fftconvolve(lp(hp(send.R, 250), 7000), ir[1])[:N]
rev = np.stack([revL, revR]); rev /= np.max(np.abs(rev)) + 1e-9

music = np.stack([mus.L, mus.R]) + np.stack([drums.L, drums.R])
music /= np.max(np.abs(music)) + 1e-9
sfx = np.stack([fx.L, fx.R]); sfx /= np.max(np.abs(sfx)) + 1e-9

out = music*.72 + sfx*.62 + rev*.12
# fade in/out
fade = np.ones(N)
fi = int(.05*SR); fade[:fi] = np.linspace(0, 1, fi)
fo0 = int(41.2*SR); fade[fo0:] = np.linspace(1, 0, N - fo0)**1.5
out *= fade
out = np.tanh(out*1.25)/np.tanh(1.25)
out /= np.max(np.abs(out)) / .95
pcm = (out.T * 32767).astype(np.int16)
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', out.shape)
