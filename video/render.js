const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/anim.html');await p.waitForFunction('window.ready()');
fs.mkdirSync('frames',{recursive:true});const fps=24,T=19;
for(let i=0;i<fps*T;i++){await p.evaluate(t=>draw(t),i/fps);await p.locator('#c').screenshot({path:`frames/f${String(i).padStart(4,'0')}.png`})}
await b.close()})();
