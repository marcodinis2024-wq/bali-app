# Música e efeitos sonoros para a colagem Timberline de 30 s (120 BPM, grelha de 0,5 s).
# Tudo sintetizado: groove com baixo e metais sintetizados, pulso de bateria, e sons de papel
# (rasgo, queda, estalo, tesoura, teclas, sino). Gera audio/score.wav (48 kHz, estéreo).
import numpy as np, wave, os
from scipy.signal import butter, sosfilt, fftconvolve
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs('audio', exist_ok=True)

SR = 48000; DUR = 30.0; N = int(SR*DUR); BEAT = .5
rng = np.random.default_rng(12)
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

# ── música ──
def bass(f, d=.32):
    t = tt(d); x = np.sin(2*np.pi*f*t)+.4*np.sin(4*np.pi*f*t)*np.exp(-t*8)
    return np.tanh(x*1.5)*np.exp(-t*7)*np.minimum(1, t/.004)
def stab(freqs, d=.35):
    t = tt(d); x = np.zeros(len(t))
    for f in freqs:
        for det in (-.1, 0, .1):
            x += np.sign(np.sin(2*np.pi*f*2**(det/12)*t))*.5+.5*np.sin(2*np.pi*f*2**(det/12)*t)
    x = lp(x, 2400)/(len(freqs)*3)
    return x*np.exp(-t*6)*np.minimum(1, t/.005)
def kick():
    t = tt(.35); f = 50+80*np.exp(-t*35)
    return np.tanh(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)*1.7)
def clap():
    t = tt(.18); x = np.zeros(len(t))
    for o in [0, .012, .024]:
        i = int(o*SR); n = len(t)-i
        x[i:] += rng.standard_normal(n)*np.exp(-t[:n]*(60 if o < .02 else 22))
    return bp(x, 1000, 3500)*.8
def hat():
    t = tt(.05); return hp(rng.standard_normal(len(t)), 7000)*np.exp(-t*110)
def pluck(f, d=.5):
    t = tt(d); x = np.sin(2*np.pi*f*t)+.3*np.sin(4*np.pi*f*t)*np.exp(-t*12)
    return x*np.exp(-t*5)*np.minimum(1, t/.002)

BAR = 2.0
CH = [[50, 57, 62, 65], [46, 53, 57, 62], [43, 50, 55, 59], [48, 55, 60, 64]]  # Dm7 · Bbmaj7 · G7 · C
ROOT = [38, 34, 31, 36]
def sec(t):
    if t < 1.5: return 'intro'
    if t < 8: return 'groove'
    if t < 13: return 'build'
    if t < 17: return 'break'
    if t < 21: return 'groove'
    if t < 24: return 'build'
    if t < 27: return 'strings'
    return 'end'

mus = Bus(); drm = Bus()
for b in range(16):
    t0 = b*BAR; c = CH[b % 4]; r = ROOT[b % 4]; s = sec(t0+.01)
    if t0 >= DUR: break
    if s in ('groove', 'build'):
        for k in range(8):
            ts = t0+k*BEAT/2
            if sec(ts) in ('end',): continue
            mus.add(bass(mtof(r+(12 if k % 4 == 3 else 0)), BEAT*.45), ts, .5)
    if s in ('groove', 'build', 'end'):
        mus.add(stab([mtof(n) for n in c[1:]], .3), t0+BAR/2, .22 if s != 'end' else .3)
        mus.add(stab([mtof(n) for n in c[1:]], .3), t0+BAR/2+BEAT*1.5, .16)
    if s == 'strings':
        mus.add(stab([mtof(n) for n in c], 1.9), t0, .22, pan=.1)
    for k in range(4):
        ts = t0+k*BEAT
        if s in ('groove', 'build') and sec(ts) == s:
            pass
        if s in ('intro',):
            continue
        for kk in [0, 2, 3]:
            mus.add(pluck(mtof(c[kk]+12)), ts+kk*BEAT/4, .07, pan=.25)
# bateria: beat no 1 e 3, claps no 2 e 4, chimbal em semicolcheias
for b in range(int(DUR/BEAT)):
    t0 = b*BEAT; s = sec(t0+.01)
    if s in ('groove', 'build') and sec(t0) != 'end':
        drm.add(kick(), t0, .85 if b % 4 in (0, 2) else .55)
        if b % 4 in (1, 3): drm.add(clap(), t0, .4)
        drm.add(hat(), t0+BEAT/2, .14, pan=.3)
    if s == 'end' and b % 4 == 0 and t0 < 27.5:
        drm.add(kick(), t0, .4)
# final: acorde e pancada
for n in [50, 57, 62, 65]: mus.add(pluck(mtof(n), 3.0), 27.0, .18)
mus.add(stab([mtof(n) for n in [38, 50, 57, 62]], 3.0), 27.0, .28)
drm.add(kick(), 27.0, .8); drm.add(kick(), 29.0, .6)

# ── efeitos de papel ──
def rip(d=.45, up=True):
    t = tt(d); x = bp(rng.standard_normal(len(t)), 900, 6000)
    x *= (.4+.6*np.abs(np.sin(2*np.pi*(13+8*t/d)*t)))*np.sin(np.pi*np.clip(t/d, 0, 1))**.6
    x /= np.max(np.abs(x))+1e-9
    return x*.7
def fall(d=.5):
    t = tt(d); f = 900*np.exp(-t*4)+120
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*3)*.35+bp(rng.standard_normal(len(t)), 500, 3000)*np.exp(-t*6)*.2
def slap(d=.18):
    t = tt(d); return (bp(rng.standard_normal(len(t)), 1200, 6000)*np.exp(-t*70)+np.sin(2*np.pi*180*t)*np.exp(-t*40)*.5)
def pop(f=900):
    t = tt(.12); ff = f*(1+.8*np.exp(-t*60)); return np.sin(2*np.pi*np.cumsum(ff)/SR)*np.exp(-t*35)*.8
def snip(d=.35):
    t = tt(d); x = hp(rng.standard_normal(len(t)), 3000)*np.exp(-t*25)*(.5+.5*np.sign(np.sin(2*np.pi*30*t)))
    return x*.6
def keys():
    t = tt(.04); return hp(rng.standard_normal(len(t)), 2500)*np.exp(-t*180)*.5
def click(f=2600):
    t = tt(.03); return np.sin(2*np.pi*f*t)*np.exp(-t*160)*.7
def bell(f=1320, d=2.2):
    t = tt(d); x = np.zeros(len(t))
    for r, a, k in [(1, 1, 1.6), (2.0, .4, 3), (3.01, .25, 5), (4.2, .12, 8)]:
        x += a*np.sin(2*np.pi*f*r*t)*np.exp(-t*k)
    return x*np.minimum(1, t/.002)*.6
def whoosh(d=.6, up=True):
    t = tt(d); n = len(t); x = bp(rng.standard_normal(n), 300, 5000)
    x *= np.sin(np.pi*np.clip(t/d, 0, 1))**1.6
    x /= np.max(np.abs(x))+1e-9
    pan = np.linspace(-.7, .7, n) if up else np.linspace(.7, -.7, n)
    return np.stack([x*np.cos((pan+1)*np.pi/4)*1.414, x*np.sin((pan+1)*np.pi/4)*1.414])*.6

fx = Bus()
fx.add(rip(.5), .0, .8)                                    # 0.00 rasgo de abertura
fx.add(fall(.5), 1.5, .5); fx.add(slap(), 1.5, .6)         # 1.50 página cai
for i, t0 in enumerate(np.arange(4.0, 8.0, .66)):           # 4–8 separadores
    fx.add(slap(), t0, .55, pan=(-.5 if i % 2 else .5)); fx.add(pop(700+60*i), t0+.02, .25)
for i, t0 in enumerate([8.0, 8.5, 9.0, 9.5, 10.0]):          # 8–13 camadas
    fx.add(slap(.22), t0, .6, pan=(i-2)*.25); fx.add(snip(.25), t0-.04, .25)
fx.add(whoosh(.5, True), 7.5, .5)
fx.add(snip(.6), 13.0, .6)                                  # 13 tesoura
for i, t0 in enumerate([13.5, 14.0, 14.5, 15.0]): fx.add(click(2000+i*200), t0, .35); fx.add(snip(.2), t0, .25)
fx.add(whoosh(.6, False), 16.7, .5)
for i, t0 in enumerate([17.0, 17.5, 18.0]): fx.add(fall(.35), t0, .4); fx.add(slap(), t0+.3, .5, pan=(i-1)*.5)
for i, t0 in enumerate(np.arange(21.0, 24.0, .5)): fx.add(pop(800+70*i), t0, .4, pan=(i % 3-1)*.5)
for i, t0 in enumerate(np.arange(24.0, 26.9, .09)):         # teclas do formulário
    if i % 3 != 2: fx.add(keys(), t0, .45, pan=(i % 5-2)*.2)
fx.add(click(2200), 26.1, .5); fx.add(bell(1760, 1.2), 25.8, .25)
fx.add(rip(.5, True), 27.0, .85)                            # 27 rasgo final
fx.add(slap(.3), 27.0, .6)
fx.add(bell(1174, 2.8), 28.8, .5); fx.add(bell(1568, 2.8), 28.85, .3)

# ── mistura ──
ir_t = tt(1.6); ir = rng.standard_normal((2, len(ir_t)))*np.exp(-ir_t*3.0)
ir[:, :int(.02*SR)] *= np.linspace(0, 1, int(.02*SR))
rev = np.stack([fftconvolve(lp(hp(fx.L, 300), 6000), ir[0])[:N], fftconvolve(lp(hp(fx.R, 300), 6000), ir[1])[:N]])
rev /= np.max(np.abs(rev))+1e-9
music = np.stack([mus.L, mus.R])+np.stack([drm.L, drm.R]); music /= np.max(np.abs(music))+1e-9
sfx = np.stack([fx.L, fx.R]); sfx /= np.max(np.abs(sfx))+1e-9
out = music*.6+sfx*.7+rev*.12
fade = np.ones(N); fi = int(.03*SR); fade[:fi] = np.linspace(0, 1, fi)
f0 = int(28.9*SR); fade[f0:] = np.linspace(1, 0, N-f0)**1.5
out *= fade; out = np.tanh(out*1.2)/np.tanh(1.2); out /= np.max(np.abs(out))/.95
with wave.open('audio/score.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out.T*32767).astype(np.int16).tobytes())
print('ok', round(DUR, 2), 's')
