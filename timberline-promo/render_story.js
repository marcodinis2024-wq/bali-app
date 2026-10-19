const { chromium } = require('playwright');
const path = require('path');
const [a,b] = process.argv.slice(2).map(Number);
process.chdir(__dirname);
const DPR = +(process.env.DPR || 1), OUT = process.env.OUT || 'frames_story';
(async () => {
  const br = await chromium.launch();
  const p = await br.newPage({ viewport:{width:1920,height:1080}, deviceScaleFactor: DPR, ignoreHTTPSErrors:true });
  p.on('pageerror', e=>console.log('ERR',e.message));
  await p.goto('file://'+process.cwd()+'/ad_story.html'); await p.evaluate(()=>window.ready); await p.waitForTimeout(400);
  for (let f=a; f<b; f++) {
    await p.evaluate(t=>render(t), f/60);
    await p.screenshot({path:`${OUT}/${String(f).padStart(5,'0')}.jpg`, type:'jpeg', quality:95});
  }
  await br.close();
})();
