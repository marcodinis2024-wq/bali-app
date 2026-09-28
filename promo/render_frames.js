const { chromium } = require('playwright');
const [a,b] = process.argv.slice(2).map(Number);
process.chdir(__dirname);
// PAGE=ad_916.html W=1080 H=1920 OUT=frames_916 para a versão vertical
const PAGE = process.env.PAGE || 'ad.html', W = +(process.env.W || 1920), H = +(process.env.H || 1080), OUT = process.env.OUT || 'frames';
(async () => {
  const br = await chromium.launch();
  const p = await br.newPage({ viewport:{width:W,height:H}, ignoreHTTPSErrors:true });
  p.on('pageerror', e=>console.log('ERR',e.message));
  await p.goto('file://'+process.cwd()+'/'+PAGE); await p.evaluate(()=>window.ready); await p.waitForTimeout(500);
  const ok = await p.evaluate(()=>['800 100px Fraunces','400 40px Yellowtail','600 20px Outfit'].every(f=>document.fonts.check(f)));
  if(!ok){ console.error('FONTS NOT LOADED'); process.exit(1); }
  for (let f=a; f<b; f++) {
    await p.evaluate(t=>render(t), f/60);
    await p.screenshot({path:`${OUT}/${String(f).padStart(5,'0')}.jpg`, type:'jpeg', quality:95});
  }
  await br.close();
})();
