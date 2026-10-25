const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.join(__dirname,'..');

test('Capacitor SystemBars handles Android WebView insets',()=>{
 const c=JSON.parse(fs.readFileSync(path.join(root,'capacitor.config.json'),'utf8'));
 assert.equal(c.plugins.SystemBars.insetsHandling,'css');
 assert.equal(c.plugins.SystemBars.initialViewportFitValueHint,'cover');
 assert.equal(c.plugins.SystemBars.hidden,false);
});

test('responsive header and bottom navigation consume native safe-area values',()=>{
 const css=fs.readFileSync(path.join(root,'web/styles.css'),'utf8');
 const html=fs.readFileSync(path.join(root,'web/index.html'),'utf8');
 assert.match(html,/viewport-fit=cover/);
 for(const rule of ['--safe-area-inset-top','--safe-area-inset-bottom','.topbar { padding-top:', '.mobile-nav { padding-bottom:', '.overlay {']){
  assert.ok(css.includes(rule),`missing ${rule}`);
 }
});
