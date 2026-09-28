const { chromium } = require('playwright');
const path = require('path');
const APP = process.env.APP_HTML || path.resolve(__dirname, '../../bali-food-drinks/index.html');
process.chdir(__dirname);
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport:{width:390,height:844}, deviceScaleFactor:2, ignoreHTTPSErrors:true, timezoneId:'Europe/Lisbon' });
  const p = await ctx.newPage();
  await p.clock.install({ time: new Date('2026-09-28T12:30:00+01:00') });
  await p.goto('file://' + APP, {waitUntil:'networkidle'});
  await p.evaluate(()=>document.fonts.ready);
  await p.addStyleTag({content:'.canopy .lf,.dot{animation:none!important}.rv{opacity:1!important;transform:none!important}::-webkit-scrollbar{display:none}.tab__count[hidden]{display:none!important}'});
  const shot = async (n, full=false) => { await p.waitForTimeout(700);
    if(full){ const h = await p.addStyleTag({content:'.tabs,.sheet,.scrim,.toast,.dialog{display:none!important}'}); await p.screenshot({path:`shots/${n}.png`, fullPage:true}); await h.evaluate(e=>e.remove()); }
    else await p.screenshot({path:`shots/${n}.png`}); };
  await shot('home'); await shot('home_full', true);
  await p.click('button.qa[data-go=menu]'); await shot('menu'); await shot('menu_full', true); 
  await p.click('.chip[data-tag=v]'); await shot('menu_vegan'); await p.click('.chip[data-tag=v]');
  for (const w of ['m','ma','man','mang','manga']) { await p.fill('#q', w); await shot('type_'+w); } await shot('menu_search'); await p.fill('#q',''); await p.evaluate(()=>{S.q='';renderMenu()});
  await p.click('.cat[data-cat=sbowls]'); await shot('menu_bowls');
  await p.click('.item >> text=Açaí Bowl'); await shot('sheet_acai');
  await p.click('#qPlus'); await shot('sheet_acai2');
  await p.click('#btnAdd'); await p.waitForTimeout(250); await p.screenshot({path:'shots/toast.png'});
  // add more items
  await p.click('.cat[data-cat=all]');
  await p.evaluate(()=>{ const i=ITEMS.findIndex(x=>x.n[0]==='Bali Brunch'); openSheet(i); });
  await shot('sheet_brunch');
  await p.click('#btnAdd');
  for (const nm of ['Caril de Camarão e Manga','Caramel Latte']) { await p.evaluate(nm=>{ openSheet(ITEMS.findIndex(x=>x.n[0]===nm)); document.querySelector('#btnAdd').click(); }, nm); }
  await p.waitForTimeout(2500);
  await p.click('#t-table'); await shot('table');
  await p.click('#swTakeaway'); await p.fill('#orderNote','Levanto às 13h15 · sem coentros no caril 🙏'); await shot('table2'); await shot('table_full', true);
  await p.click('#t-info'); await shot('info');
  await p.click('#t-home'); await p.click('.lang button[data-lang=en]'); await shot('home_en');
  await p.click('#t-menu'); await shot('menu_en');
  await p.click('#t-home'); await p.click('.lang button[data-lang=pt]'); console.log(JSON.stringify(await p.evaluate(()=>({rev:document.querySelector('.revtop').getBoundingClientRect().top+scrollY, rail:document.querySelector('#railSignature').getBoundingClientRect().top+scrollY}))));
  await b.close();
})();
