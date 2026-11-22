import numpy as np, wave
SR=44100; T=22.0; n=int(SR*T); t=np.arange(n)/SR
L=np.zeros(n); R=np.zeros(n)
rng=np.random.default_rng(3)
def add(sig,start,pan=0.0,gain=1.0):
    i=int(start*SR); sig=sig[:max(0,n-i)]
    L[i:i+len(sig)]+=sig*gain*(1-pan)/2*1.4; R[i:i+len(sig)]+=sig*gain*(1+pan)/2*1.4
def env(d,a=.01,r=.3):
    x=np.arange(int(d*SR))/SR; e=np.minimum(x/a,1)*np.exp(-x/r); return e
def tone(f,d,a=.01,r=.4,harm=(1,.4,.2)):
    x=np.arange(int(d*SR))/SR
    s=sum(h*np.sin(2*np.pi*f*(k+1)*x) for k,h in enumerate(harm))
    return s*env(d,a,r)
def lp(x,k):  # simple one-pole low-pass
    y=np.zeros_like(x); a=1/(1+k); acc=0
    for i in range(len(x)): acc+=a*(x[i]-acc); y[i]=acc
    return y
def fade(x,a,b,t0,t1):  # gain ramp in time
    return x*np.clip((t-t0)/(t1-t0),0,1)*(b-a)+x*a if False else x
# 1) city ambience 0-4.5 (noise, fades out with blackout)
noise=rng.standard_normal(int(SR*4.8)); amb=lp(noise,60)*0.25
amb*=np.interp(np.arange(len(amb))/SR,[0,2,4,4.8],[1,.9,.1,0]); add(amb,0,0,1)
# soft opening pad (Am)
for f in (110,164.8,220):
    x=np.arange(int(SR*4.5))/SR; add(np.sin(2*np.pi*f*x)*np.interp(x,[0,1,3.5,4.5],[0,.08,.08,0]),0,0,1)
# 2) blackout: descending sweep + sub boom
d=2.4; x=np.arange(int(d*SR))/SR; f=np.interp(x,[0,d],[520,38]); ph=2*np.pi*np.cumsum(f)/SR
add(np.sin(ph)*np.interp(x,[0,.1,d],[0,.35,0]),2.0,0,1)
x=np.arange(int(1.6*SR))/SR; add(np.sin(2*np.pi*(55-20*x/1.6)*x)*np.exp(-x*2.2)*.9,3.7,0,1)
for k in range(9): add(tone(900-70*k,.12,.002,.04,(1,.3))*.15,2.0+k*.22,rng.uniform(-.8,.8),1)  # window clicks off
# 3) tension drone 4-9
x=np.arange(int(5*SR))/SR; dr=np.sin(2*np.pi*55*x)*.18+np.sin(2*np.pi*82.4*x)*.08
add(dr*np.interp(x,[0,.8,4.2,5],[0,1,1,0]),4.2,0,1)
# heartbeat-ish pulses
for b in np.arange(4.6,8.8,1.0): 
    xx=np.arange(int(.3*SR))/SR; add(np.sin(2*np.pi*50*xx)*np.exp(-xx*14)*.4,b,0,1)
# 4) apartment lights: click + warm rising chime at 5.2
add(np.random.default_rng(1).standard_normal(int(.02*SR))*np.linspace(1,0,int(.02*SR))*.3,5.1,0,1)
for i,fr in enumerate((392,523.3,659.3,784)): add(tone(fr,2.2,.01,.9)*.22,5.3+i*.18,0,1)
# 5) room/hybrid music 9-19.4: pad chords + arpeggio (C - G - Am - F), 105 bpm
bpm=105; beat=60/bpm; chords=[(130.8,164.8,196),(98,123.5,146.8),(110,130.8,164.8),(87.3,110,130.8)]
arp=[[261.6,329.6,392,523.3],[196,246.9,293.7,392],[220,261.6,329.6,440],[174.6,220,261.6,349.2]]
start=9.0; bar=beat*4; ci=0; tt=start
while tt<19.2:
    ch=chords[ci%4]; d=bar+.3
    x=np.arange(int(d*SR))/SR
    pad=sum(np.sin(2*np.pi*f*x)+.4*np.sin(2*np.pi*f*2*x) for f in ch)*np.minimum(x/.4,1)*np.exp(-np.maximum(x-bar,0)*8)
    add(pad*.07,tt,0,1)
    for j in range(8):
        fr=arp[ci%4][j%4]*(2 if j>=4 else 1)/ (1 if j<4 else 2)
        add(tone(fr,.5,.005,.18,(1,.5,.15))*.16,tt+j*beat/2,(-.5 if j%2 else .5),1)
    add(np.sin(2*np.pi*55*np.arange(int(.35*SR))/SR)*np.exp(-np.arange(int(.35*SR))/SR*9)*.5,tt,0,1)       # kick on 1
    add(np.sin(2*np.pi*55*np.arange(int(.35*SR))/SR)*np.exp(-np.arange(int(.35*SR))/SR*9)*.4,tt+2*beat,0,1)  # kick on 3
    tt+=bar; ci+=1
# electric whoosh when energy starts flowing (9.7) and sun shimmer (16)
w=lp(rng.standard_normal(int(1.2*SR)),6)*np.interp(np.arange(int(1.2*SR))/SR,[0,.6,1.2],[0,.4,0]); add(w,9.4,0,1)
for i,fr in enumerate((1046.5,1318.5,1568,2093)): add(tone(fr,1.6,.01,.6,(1,.2))*.08,16.1+i*.12,0.6*(-1)**i,1)
# 6) end card: resolved chord + sparkle at 19.4
for f in (261.6,329.6,392,523.3): add(tone(f,2.8,.02,1.3,(1,.35,.12))*.2,19.4,0,1)
add(tone(130.8,2.8,.02,1.4,(1,.4))*.25,19.4,0,1)
for i,fr in enumerate((1568,2093,2637)): add(tone(fr,1.2,.005,.4,(1,.1))*.07,19.9+i*.15,(-.6 if i%2 else .6),1)
# master: fade in/out, normalize
m=np.interp(t,[0,.5,T-1.5,T],[0,1,1,0]); L*=m; R*=m
pk=max(abs(L).max(),abs(R).max()); L=L/pk*.85; R=R/pk*.85
s=(np.stack([L,R],1)*32767).astype('<i2')
with wave.open('trilha.wav','wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(s.tobytes())
