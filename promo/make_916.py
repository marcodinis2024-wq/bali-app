# Gera ad_916.html (1080x1920) a partir de ad.html (1920x1080).
# Mesma linha temporal e mesmo áudio; muda só o layout de cada cena.
import os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
s = open('ad.html', encoding='utf-8').read()

def R(old, new, count=1):
    global s
    n = s.count(old)
    assert n >= 1, f'não encontrado: {old[:70]}'
    if count == 1: assert n == 1, f'ambíguo ({n}x): {old[:70]}'
    s = s.replace(old, new)

# ── palco ──
R('html,body{width:1920px;height:1080px;', 'html,body{width:1080px;height:1920px;')
R('#stage{position:absolute;inset:0;width:1920px;height:1080px;', '#stage{position:absolute;inset:0;width:1080px;height:1920px;')
R("$('#grain').style.width='2120px';$('#grain').style.height='1280px';", "$('#grain').style.width='1280px';$('#grain').style.height='2120px';")
R('<canvas id="grain" width="1024" height="640">', '<canvas id="grain" width="640" height="1024">')
R('for(let i=0;i<id.data.length;i+=4)', 'for(let i=0;i<id.data.length;i+=4)')
s = s.replace('createImageData(1024,640)', 'createImageData(640,1024)')
R("gctx.putImageData(GR[gi],0,0);", "gctx.putImageData(GR[gi],0,0);")

# fundos / blobs
for a in ['id="s2burst" style="left:1340px"', 'id="s4burst" style="left:1360px"', 'id="s6burst" style="left:560px"']:
    R(a, a.split(' style')[0] + ' style="left:540px;top:1250px"')
R('<div class="blob" style="left:980px;top:120px;width:700px;height:700px;background:rgba(55,154,151,.28)"></div>',
  '<div class="blob" style="left:190px;top:900px;width:700px;height:700px;background:rgba(55,154,151,.28)"></div>')
R('<div class="blob" style="left:1400px;top:620px;width:420px;height:420px;background:rgba(239,162,63,.30)"></div>',
  '<div class="blob" style="left:640px;top:1450px;width:420px;height:420px;background:rgba(239,162,63,.30)"></div>')
R('<div class="blob" style="left:1100px;top:80px;width:600px;height:600px;background:rgba(239,162,63,.22)"></div>',
  '<div class="blob" style="left:520px;top:180px;width:600px;height:600px;background:rgba(239,162,63,.22)"></div>')
R('<div class="blob" style="left:900px;top:600px;width:500px;height:500px;background:rgba(111,164,99,.22)"></div>',
  '<div class="blob" style="left:-80px;top:1200px;width:500px;height:500px;background:rgba(111,164,99,.22)"></div>')
R('<div class="blob" style="left:40px;top:180px;width:700px;height:700px;background:rgba(55,154,151,.20)"></div>',
  '<div class="blob" style="left:-100px;top:180px;width:700px;height:700px;background:rgba(55,154,151,.20)"></div>')
R('<div class="blob" style="left:1100px;top:100px;width:800px;height:800px;background:rgba(31,168,85,.16)"></div>',
  '<div class="blob" style="left:300px;top:800px;width:800px;height:800px;background:rgba(31,168,85,.16)"></div>')

# tamanhos de texto para a largura de 1080
R('id="fome" style="font-size:300px;', 'id="fome" style="font-size:250px;')
R('id="s0tag" style="font:600 60px Fraunces,serif;color:var(--paper2);white-space:nowrap;text-align:center"',
  'id="s0tag" style="font:600 64px/1.15 Fraunces,serif;color:var(--paper2);width:860px;text-align:center"')
R('id="s1h1" style="font-size:118px;', 'id="s1h1" style="font-size:104px;')
R('id="s1h2" style="font-size:118px;', 'id="s1h2" style="font-size:104px;')
R('style="color:var(--mango);font-size:150px;font-weight:400">mão.', 'style="color:var(--mango);font-size:132px;font-weight:400">mão.')
R('id="s1sub" style="font:400 38px Outfit;', 'id="s1sub" style="font:400 36px Outfit;')
R('id="s2num" style="font-size:330px;', 'id="s2num" style="font-size:280px;')
R("font-size:136px;color:var(--t900);white-space:nowrap';", "font-size:112px;color:var(--t900);white-space:nowrap';")
R('id="s3sub" style="font:400 36px Outfit;', 'id="s3sub" style="font:400 31px Outfit;')
R('id="s4h1" style="font-size:124px;', 'id="s4h1" style="font-size:108px;')
R('id="s4h2" style="font-size:124px;', 'id="s4h2" style="font-size:108px;')
R('style="color:var(--mango);font-size:156px;font-weight:400">prato.', 'style="color:var(--mango);font-size:138px;font-weight:400">prato.')
R('id="s4sub" style="font:400 38px Outfit;', 'id="s4sub" style="font:400 34px Outfit;')
R('id="s5h" style="font-size:150px;', 'id="s5h" style="font-size:118px;')
R('style="color:var(--mango);font-size:190px;font-weight:400">mesa!', 'style="color:var(--mango);font-size:150px;font-weight:400">mesa!')
R('id="s5sub" style="font:400 38px Outfit;', 'id="s5sub" style="font:400 34px Outfit;')
R('.check{display:flex;align-items:center;gap:22px;font:600 38px Outfit;', '.check{display:flex;align-items:center;gap:20px;font:600 36px Outfit;')
R('id="s7h1" style="font-size:96px;', 'id="s7h1" style="font-size:108px;')
R('id="s7h2" style="font-size:96px;', 'id="s7h2" style="font-size:108px;')
R('id="s7sub" style="font:400 32px/1.35 Outfit;color:#3E5F5B;width:430px"', 'id="s7sub" style="font:400 34px/1.35 Outfit;color:#3E5F5B;width:900px"')
R('.chat{position:absolute;left:0;top:0;width:680px;height:800px;', '.chat{position:absolute;left:0;top:0;width:700px;height:760px;')
R('id="s9h" style="font-size:84px;color:var(--paper2);white-space:nowrap;font-weight:700"',
  'id="s9h" style="font-size:86px;line-height:1.08;color:var(--paper2);width:900px;text-align:center;font-weight:700"')
R('id="s9cta" style="font:800 44px Outfit;padding:26px 50px"', 'id="s9cta" style="font:800 40px Outfit;padding:26px 44px"')
R('id="s9info" style="font:500 30px Outfit;color:rgba(248,251,246,.85);white-space:nowrap;display:flex;gap:44px;align-items:center"',
  'id="s9info" style="font:500 32px/1.6 Outfit;color:rgba(248,251,246,.85);white-space:nowrap;display:flex;flex-direction:column;gap:0;align-items:center"')
R('<span>Rua Machado dos Santos 13, Leiria</span><span style="color:var(--mango)">●</span><span>@balifoodanddrinks</span><span style="color:var(--mango)">●</span><span>Pet friendly</span>',
  '<span>Rua Machado dos Santos 13, Leiria</span><span>@balifoodanddrinks · Pet friendly</span>')

# folhas nos cantos
R("""const cornerLeaves=[
 {x:120,y:80,fx:-300,fy:-300,r:140,dr:-60,w:260,f:'#4FA88F',op:.55},
 {x:300,y:-20,fx:0,fy:-500,r:170,dr:40,w:200,f:'#8FBE81',op:.45},
 {x:1800,y:90,fx:2200,fy:-300,r:-140,dr:60,w:280,f:'#4FA88F',op:.55},
 {x:1600,y:-30,fx:1700,fy:-500,r:-165,dr:-40,w:190,f:'#8FBE81',op:.45},
 {x:110,y:1000,fx:-300,fy:1400,r:40,dr:60,w:250,f:'#8FBE81',op:.5},
 {x:1820,y:990,fx:2300,fy:1400,r:-40,dr:-60,w:270,f:'#4FA88F',op:.55},
 {x:1690,y:1120,fx:1800,fy:1600,r:-15,dr:-60,w:180,f:'#6FA463',op:.45},
 {x:260,y:1120,fx:200,fy:1600,r:15,dr:60,w:170,f:'#6FA463',op:.45},
];""", """const cornerLeaves=[
 {x:80,y:90,fx:-300,fy:-300,r:140,dr:-60,w:260,f:'#4FA88F',op:.55},
 {x:260,y:-20,fx:0,fy:-500,r:170,dr:40,w:200,f:'#8FBE81',op:.45},
 {x:1000,y:100,fx:1400,fy:-300,r:-140,dr:60,w:280,f:'#4FA88F',op:.55},
 {x:820,y:-30,fx:900,fy:-500,r:-165,dr:-40,w:190,f:'#8FBE81',op:.45},
 {x:70,y:1840,fx:-300,fy:2300,r:40,dr:60,w:250,f:'#8FBE81',op:.5},
 {x:1010,y:1830,fx:1400,fy:2300,r:-40,dr:-60,w:270,f:'#4FA88F',op:.55},
 {x:860,y:1960,fx:900,fy:2400,r:-15,dr:-60,w:180,f:'#6FA463',op:.45},
 {x:220,y:1960,fx:200,fy:2400,r:15,dr:60,w:170,f:'#6FA463',op:.45},
];""")
R("""{x:80,y:60,fx:-300,fy:-300,r:140,dr:-60,w:240,f:'#4FA88F',op:.35},
 {x:40,y:1000,fx:-300,fy:1400,r:40,dr:60,w:230,f:'#8FBE81',op:.3},
 {x:1870,y:980,fx:2300,fy:1400,r:-40,dr:-60,w:220,f:'#4FA88F',op:.3}]);""",
  """{x:1010,y:60,fx:1400,fy:-300,r:-140,dr:60,w:240,f:'#4FA88F',op:.35},
 {x:40,y:1840,fx:-300,fy:2300,r:40,dr:60,w:230,f:'#8FBE81',op:.3},
 {x:1040,y:1820,fx:1400,fy:2300,r:-40,dr:-60,w:220,f:'#4FA88F',op:.3}]);""")
R("""{x:1850,y:40,fx:2200,fy:-300,r:-140,dr:60,w:240,f:'#8FBE81',op:.35},
 {x:40,y:1040,fx:-300,fy:1400,r:40,dr:60,w:220,f:'#8FBE81',op:.3}]);""",
  """{x:1030,y:40,fx:1400,fy:-300,r:-140,dr:60,w:240,f:'#8FBE81',op:.35},
 {x:40,y:1860,fx:-300,fy:2300,r:40,dr:60,w:220,f:'#8FBE81',op:.3}]);""")

# chips: quebra de linha automática em 980 px
R("""const chipPos=[];(()=>{const rows=[[0,1,2,3],[4,5,6],[7,8,9,10],[11,12,13],[14,15]];
 const widths=CH.map(c=>c.length*15.5+80);
 rows.forEach((r,ri)=>{const tw=r.reduce((a,i)=>a+widths[i]+18,-18);let x=1340-tw/2;r.forEach(i=>{chipPos[i]={x:x+widths[i]/2,y:720+ri*84};x+=widths[i]+18})})})();""",
  """const chipPos=[];(()=>{chipEls.forEach(c=>{c.style.fontSize='25px';c.style.padding='11px 22px'});
 const widths=CH.map(c=>c.length*13.8+68);const rows=[[]];let w=0;
 CH.forEach((c,i)=>{if(w+widths[i]>1000&&rows[rows.length-1].length){rows.push([]);w=0}rows[rows.length-1].push(i);w+=widths[i]+14});
 rows.forEach((r,ri)=>{const tw=r.reduce((a,i)=>a+widths[i]+14,-14);let x=540-tw/2;r.forEach(i=>{chipPos[i]={x:x+widths[i]/2,y:640+ri*70};x+=widths[i]+14})})})();""")

# telemóvel principal: fica ao centro, em baixo; transições por zoom/rotação
R("""const MK=[
 // t,   x,    y,   s,   ry,  rz
 [0,    2500, 560, .8, -45,  10],
 [4.0,  2500, 560, .8, -45,  10],
 [4.75, 1330, 545, 1,  -14, -3, E.expo],
 [7.55, 1330, 545, 1,  -12, -2],
 [8.15, 560,  545, 1,   14,  3, E.expo],
 [11.9, 560,  545, 1,   12,  2],
 [12.2, 560,  545, 1.06, 10, 1.5, E.out],
 [15.7, 560,  545, 1.06, 10, 1.5],
 [16.2, 1360, 545, 1.02,-12, -2, E.expo],
 [19.7, 1360, 545, 1.05,-10, -2],
 [20.2, 1360, 545, 1.08,-6,  -1, E.out],
 [23.65,1360, 545, 1.08,-6,  -1],
 [24.15,560,  545, 1,   14,  3, E.expo],
 [27.6, 560,  545, 1.03, 12, 2],
 [28.1, 360,  545, .96,  18, 3, E.expo],
 [31.65,360,  545, .96,  16, 2],
 [32.2, 960,  560, .86,  0,  0, E.expo],
 [35.55,960,  560, .86,  0,  0],
 [36.0, 960,  1800,.7,   0,  0, E.expoIn],
 [42,   960,  1800,.7,   0,  0],
];""", """const MK=[
 // t,   x,    y,    s,   ry,  rz
 [0,    540,  2700, .8, -30,  10],
 [4.0,  540,  2700, .8, -30,  10],
 [4.75, 560,  1250, .98,-12, -3, E.expo],
 [7.55, 560,  1250, .98,-10, -2],
 [8.15, 540,  1330, .9,  12,  3, E.expo],
 [11.9, 540,  1330, .9,  10,  2],
 [12.2, 540,  1340, .93, 8,  1.5, E.out],
 [15.7, 540,  1340, .93, 8,  1.5],
 [16.2, 560,  1250, 1.02,-12, -2, E.expo],
 [19.7, 560,  1250, 1.04,-10, -2],
 [20.2, 560,  1250, 1.08,-6,  -1, E.out],
 [23.65,560,  1250, 1.08,-6,  -1],
 [24.15,540,  1360, .9,  12,  3, E.expo],
 [27.6, 540,  1360, .92, 10,  2],
 [28.1, 210,  1560, .52, 16, -6, E.expo],
 [31.65,210,  1560, .52, 14, -6],
 [32.2, 540,  1180, .8,  0,  0, E.expo],
 [35.55,540,  1180, .8,  0,  0],
 [36.0, 540,  2900, .7,  0,  0, E.expoIn],
 [42,   540,  2900, .7,  0,  0],
];""")
# desfoque de movimento também na vertical
R(""" const vx=(track(MK,t+1/60)[0]-x)*60;""", """ const nx=track(MK,t+1/60);const vx=Math.hypot(nx[0]-x,nx[1]-y)*60;""")

# transições
R("$('#s0').style.transform=`translateX(${-wp*1920}px)`", "$('#s0').style.transform=`translateY(${-wp*1920}px)`")
R("s1.style.transform=`translateX(${(1-wp)*1920}px)`", "s1.style.transform=`translateY(${(1-wp)*1920}px)`")
R("circ(s2,t,7.7,.55,560,545);", "circ(s2,t,7.7,.55,540,1330);")
R("circ(s4,t,15.7,.55,1360,545);", "circ(s4,t,15.7,.55,560,1250);")
R("circ(s6,t,23.6,.55,560,545);", "circ(s6,t,23.6,.55,540,1360);")
R("circ(s7,t,27.25,.55,560,545+(580-422));", "circ(s7,t,27.25,.55,540,1360+(580-422)*.92);")
R("circ(s9,t,35.9,.6,960,540);", "circ(s9,t,35.9,.6,540,960);")
R("function slideIn(el,t,t0,d,dir){const p=E.expo(P(t,t0,t0+d));el.style.clipPath='none';el.style.transform=p>=1?'none':`translate(${dir[0]*(1-p)*1920}px,${dir[1]*(1-p)*1080}px)`}",
  "function slideIn(el,t,t0,d,dir){const p=E.expo(P(t,t0,t0+d));el.style.clipPath='none';el.style.transform=p>=1?'none':`translate(${dir[0]*(1-p)*1080}px,${dir[1]*(1-p)*1920}px)`}")

# S0
R("S('#fome',{x:960,y:520-fo*40,", "S('#fome',{x:540,y:900-fo*40,")
R("S(id,{x:960,y:520,s:.4+E.out(p)*6,", "S(id,{x:540,y:900,s:.4+E.out(p)*6,")
R("const orbit=[[-600,-230],[600,-250],[-700,120],[700,110],[-380,330],[380,340]];", "const orbit=[[-300,-420],[300,-460],[-340,-120],[340,-80],[-260,330],[260,360]];")
R("S(d,{x:960+orbit[i][0]*e*(1+out*1.4),y:520+orbit[i][1]*e*(1+out*1.4)+bob,", "S(d,{x:540+orbit[i][0]*e*(1+out*1.4),y:900+orbit[i][1]*e*(1+out*1.4)+bob,")
R("S('#s0stamp',{x:960,y:430,", "S('#s0stamp',{x:540,y:800,")
R("S('#s0tag',{x:960,y:790,", "S('#s0tag',{x:540,y:1180,")
# S1
R("S('#s1eb',{x:160,y:300-ex*60,", "S('#s1eb',{x:80,y:290-ex*60,")
R("S('#s1h1',{x:150,y:420-ex*60,", "S('#s1h1',{x:70,y:395-ex*60,")
R("S('#s1h2',{x:150,y:545-ex*60,", "S('#s1h2',{x:70,y:505-ex*60,")
R("S('#s1swoosh',{x:560,y:620-ex*60,", "S('#s1swoosh',{x:450,y:572-ex*60,")
R("S('#s1sub',{x:156,y:720+", "S('#s1sub',{x:76,y:660+")
R("const C=[['#s1c1',4.9,1620,230],['#s1c2',5.25,1010,190],['#s1c3',5.6,1650,700],['#s1c4',5.95,1010,860]];",
  "const C=[['#s1c1',4.9,830,830],['#s1c2',5.25,270,1000],['#s1c3',5.6,900,1380],['#s1c4',5.95,300,1560]];")
R("S(id,{x:x+o*(x>1300?600:-300),", "S(id,{x:x+o*(x>540?600:-600),")
# S2
R("S('#s2num',{x:1340,y:330-ex*100,", "S('#s2num',{x:540,y:360-ex*100,")
R("S('#s2lab',{x:1340,y:540-ex*100,", "S('#s2lab',{x:540,y:540-ex*100,")
# S3
R("S(d,{x:1060,y:250+i*165-ex*80,", "S(d,{x:80,y:320+i*132-ex*80,")
R("S(d,{x:1060+[0,165,370,500][i],y:780-ex*80+", "S(d,{x:80+[0,165,370,500][i],y:720-ex*80+")
R("S('#s3sub',{x:1062,y:880+", "S('#s3sub',{x:82,y:810+")
# S4
R("S('#s4eb',{x:160,y:300-ex*60,", "S('#s4eb',{x:80,y:290-ex*60,")
R("S('#s4h1',{x:150,y:420-ex*60,", "S('#s4h1',{x:70,y:395-ex*60,")
R("S('#s4h2',{x:150,y:550-ex*60,", "S('#s4h2',{x:70,y:510-ex*60,")
R("S('#s4sub',{x:156,y:690+", "S('#s4sub',{x:76,y:640+")
R("S('#s4stk',{x:330,y:880+", "S('#s4stk',{x:175,y:1500+")
R("S('#s4price',{x:960,y:820+", "S('#s4price',{x:900,y:1060+")
# S5
R("S('#s5eb',{x:160,y:330-ex*60,", "S('#s5eb',{x:80,y:300-ex*60,")
R("S('#s5h',{x:150,y:470-ex*60,", "S('#s5h',{x:70,y:420-ex*60,")
R("S('#s5sub',{x:156,y:600+", "S('#s5sub',{x:76,y:545+")
R("const tabX=1360+(243-195)*1.08, tabY=545+(810-422)*1.08;", "const tabX=560+(243-195)*1.08, tabY=1250+(810-422)*1.08;")
R("const sx=420+i*60, sy=760+i*95;", "const sx=300+i*60, sy=700+i*85;")
# S6
R("S('#s6h1',{x:1000,y:260-ex*60,", "S('#s6h1',{x:70,y:280-ex*60,")
R("S('#s6h2',{x:1000,y:390-ex*60,", "S('#s6h2',{x:70,y:400-ex*60,")
R("S(id,{x:1010+(1-e)*-80,y:540+i*95-ex*60,", "S(id,{x:80+(1-e)*-80,y:530+i*78-ex*60,")
R("S('#s6tot',{x:1010,y:880-ex*60,", "S('#s6tot',{x:80,y:790-ex*60,")
R('id="s6tot" style="font:800 58px Outfit;padding:24px 44px;gap:26px"', 'id="s6tot" style="font:800 50px Outfit;padding:18px 38px;gap:22px"')
# S7
R("S('#s7eb',{x:680,y:330-ex*60,", "S('#s7eb',{x:80,y:290-ex*60,")
R("S('#s7h1',{x:672,y:420-ex*60,", "S('#s7h1',{x:70,y:395-ex*60,")
R("S('#s7h2',{x:672,y:520-ex*60,", "S('#s7h2',{x:70,y:505-ex*60,")
R("S('#s7sub',{x:676,y:660+", "S('#s7sub',{x:76,y:610+")
R("S('#s7chat',{x:1480+(1-cp)*700-ex*0,y:545+ex*900,", "S('#s7chat',{x:590+(1-cp)*900,y:1140+ex*1200,")
R("const bx=lerp(360,1560,e), by=lerp(545+150,560,e)", "const bx=lerp(210,650,e), by=lerp(1560+80,1160,e)")
R("S('#s7bub',{x:bx,y:by+ex*900,", "S('#s7bub',{x:bx,y:by+ex*1200,")
R("S('#s7stamp',{x:1540,y:880+ex*900,", "S('#s7stamp',{x:730,y:1560+ex*1200,")
# S8
R("const L=[['#s8l1',32.5,960,95],['#s8l2',33.0,330,260],['#s8l3',33.5,1590,260],['#s8l4',34.0,330,820],['#s8l5',34.5,1590,820]];",
  "const L=[['#s8l1',32.5,540,470],['#s8l2',33.0,320,600],['#s8l3',33.5,760,700],['#s8l4',34.0,330,1640],['#s8l5',34.5,750,1740]];")
R("S('#s8t',{x:960,y:1010+ex*300,", "S('#s8t',{x:540,y:320-ex*300,")
R("phoneT(PL,{x:lerp(-400,520,sp),y:600+so*1300+", "phoneT(PL,{x:lerp(-400,250,sp),y:1250+so*1300+")
R("phoneT(PR,{x:lerp(2320,1400,sp),y:600+so*1300+", "phoneT(PR,{x:lerp(1480,830,sp),y:1250+so*1300+")
s = s.replace("s:.74,ry:28,rz:-6", "s:.6,ry:28,rz:-6").replace("s:.74,ry:-28,rz:6", "s:.6,ry:-28,rz:6")
R("ex*(y>500?500:-500)", "ex*(y>1000?700:-700)")
# S9
R("S('#s9stamp',{x:960,y:330,", "S('#s9stamp',{x:540,y:640,")
R("S('#s9h',{x:960,y:640,", "S('#s9h',{x:540,y:1040,")
R("S('#s9cta',{x:960,y:790,", "S('#s9cta',{x:540,y:1270,")
R("S('#s9info',{x:960,y:910+", "S('#s9info',{x:540,y:1420+")
R("const orb=[[-560,-150],[560,-150],[-700,120],[700,120],[-430,-330],[430,-330]];", "const orb=[[-370,-250],[370,-250],[-380,90],[380,90],[-200,-400],[200,-400]];")
R("S(d,{x:960+orb[i][0],y:360+orb[i][1]", "S(d,{x:540+orb[i][0],y:640+orb[i][1]")

open('ad_916.html', 'w', encoding='utf-8').write(s)
print('ok')
