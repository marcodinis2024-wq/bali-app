const { chromium } = require('playwright');
const [a,b] = process.argv.slice(2).map(Number);
process.chdir(__dirname);
(async () => {
  const br = await chromium.launch();
  const p = await br.newPage({ viewport:{width:1920,height:1080}, ignoreHTTPSErrors:true });
  p.on('pageerror', e=>console.log('ERR',e.message));
  await p.goto('file://'+process.cwd()+'/ad.html'); await p.evaluate(()=>window.ready); await p.waitForTimeout(500);
  for (let f=a; f<b; f++) {
    await p.evaluate(t=>render(t), f/60);
    await p.screenshot({path:`frames/${String(f).padStart(5,'0')}.jpg`, type:'jpeg', quality:95});
  }
  await br.close();
})();
