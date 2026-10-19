const { chromium } = require('playwright');
const path = require('path');
const [a,b] = process.argv.slice(2).map(Number);
process.chdir(__dirname);
const DPR = +(process.env.DPR || 1), VW = +(process.env.VW || 1920), VH = +(process.env.VH || 1080), OUT = process.env.OUT || 'frames_story';
(async () => {
  const br = await chromium.launch();
  const p = await br.newPage({ viewport:{width:VW,height:VH}, deviceScaleFactor: DPR, ignoreHTTPSErrors:true });
  p.on('pageerror', e=>console.log('ERR',e.message));
  await p.goto('file://'+process.cwd()+'/ad_story_916.html'); await p.evaluate(()=>window.ready); await p.waitForTimeout(400);
  for (let f=a; f<b; f++) {
    await p.evaluate(t=>render(t), f/60);
    await p.screenshot({path:`${OUT}/${String(f).padStart(5,'0')}.jpg`, type:'jpeg', quality:95});
  }
  await br.close();
})();
