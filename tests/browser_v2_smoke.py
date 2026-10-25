from playwright.sync_api import sync_playwright
from pathlib import Path
import re
root=Path(__file__).resolve().parent.parent
html=(root/'web/index.html').read_text()
html=re.sub(r'<link rel="stylesheet"[^>]*>', '', html)
html=re.sub(r'<script src="[^"]+"></script>', '', html)
mock="""
Object.defineProperty(window,'indexedDB',{configurable:true,value:{open(){const req={};setTimeout(()=>{req.result={objectStoreNames:{contains:()=>true},transaction(){const txn={oncomplete:null};txn.objectStore=()=>({get(){const q={};setTimeout(()=>{q.result=window.__data;q.onsuccess?.()},5);return q},put(v){window.__data=structuredClone(v);setTimeout(()=>txn.oncomplete?.(),5);return {}}});return txn}};req.onsuccess?.()},4);return req}}});
"""
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 errors=[]
 def boot(w,h):
  page=browser.new_page(viewport={'width':w,'height':h},accept_downloads=True)
  page.on('pageerror',lambda err:errors.append(str(err)))
  page.set_content(html)
  page.add_style_tag(content=(root/'web/styles.css').read_text())
  page.add_script_tag(content=mock)
  for name in ['core.js','exports.js','app.js']:
   page.add_script_tag(content=(root/'web'/name).read_text())
  page.wait_for_timeout(200)
  return page
 page=boot(1440,900)
 print('start',page.locator('h1').first.inner_text())
 assert page.locator('.sidebar [data-page="products"]').count()==0
 page.locator('.sidebar [data-page="sale"]').click()
 assert page.locator('#saleName').count()==0
 assert page.locator('#saleRemarks').count()==0
 assert page.locator('[data-line-field="qty"]').count()==0
 page.locator('#saleFund').select_option('Food')
 page.locator('#saleAmount').fill('2500.00')
 page.locator('#saleForm button[type=submit]').click()
 page.wait_for_timeout(150)
 print('food sale balance',page.locator('.stat-card.accent .stat-value').first.inner_text())
 page.locator('.sidebar [data-page="sale"]').click()
 page.locator('#saleFund').select_option('Goods')
 page.locator('#saleAmount').fill('500')
 page.locator('#saleForm button[type=submit]').click()
 page.wait_for_timeout(150)
 page.locator('.sidebar [data-page="expense"]').click()
 page.locator('#expenseFund').select_option('Food')
 page.locator('#expenseAmount').fill('800')
 page.locator('#expenseDescription').fill('Rice ingredients')
 page.locator('#expenseForm button[type=submit]').click()
 page.wait_for_timeout(150)
 page.locator('.sidebar [data-page="coop"]').click()
 print('coop title',page.locator('h1').first.inner_text())
 page.locator('[data-action="member-add"]').click()
 page.locator('#memberName').fill('Maria Santos')
 page.locator('#memberRole').fill('Treasurer')
 page.locator('#memberForm button[type=submit]').click()
 page.wait_for_timeout(140)
 print('members', page.locator('.member-row').count())
 page.locator('[data-action="coop-money"]').click()
 page.locator('#coopAmount').fill('1000')
 page.locator('#coopReason').fill('Coop contributions')
 page.locator('#coopMember').select_option(index=1)
 page.locator('#coopForm button[type=submit]').click()
 page.wait_for_timeout(180)
 page.locator('.sidebar [data-page="expense"]').click()
 page.locator('#expenseFund').select_option('Coop')
 page.locator('#expenseAmount').fill('300')
 page.locator('#expenseDescription').fill('Coop repair')
 page.locator('#expenseForm button[type=submit]').click()
 page.wait_for_timeout(140)
 page.locator('.sidebar [data-page="dashboard"]').click()
 page.screenshot(path=str(root/'tests'/'v2-desktop.png'),full_page=True)
 values=page.locator('.fund-card strong').all_inner_texts()
 print('funds',values)
 assert ['1,700.00','500.00','700.00','0.00']==[x.replace('₱','').replace('PHP','').strip() for x in values],values
 assert '2,900.00' in page.locator('.stat-card.accent .stat-value').first.inner_text()
 page.locator('.sidebar [data-page="transactions"]').click()
 assert 'Coop repair' in page.locator('tbody').inner_text()
 assert 'Cooperative Money' in page.locator('tbody').inner_text()
 page.locator('.sidebar [data-page="coop"]').click()
 page.locator('[data-action="member-toggle"]').click()
 page.locator('[data-action="confirm-run"]').click()
 page.wait_for_timeout(120)
 assert page.locator('.member-row.archived').count()==1
 assert 'Maria Santos' in page.locator('.member-row').inner_text()
 page.locator('.sidebar [data-page="reports"]').click()
 page.locator('#reportType').select_option('expenses')
 page.locator('[data-action="report-update"]').click()
 assert 'Paid from' in page.locator('#reportPreview').inner_text()
 for fmt in ['xlsx','csv','pdf']:
  with page.expect_download(timeout=15000) as dl:
   page.locator(f'[data-action="export-report"][data-format="{fmt}"]').click()
  f=root/'tests'/f'v2-report.{fmt}'
  dl.value.save_as(f)
  print('export',fmt,f.stat().st_size)
 mobile=boot(390,844)
 mobile.screenshot(path=str(root/'tests'/'v2-mobile.png'),full_page=True)
 assert not mobile.evaluate('document.documentElement.scrollWidth>window.innerWidth')
 mobile.locator('#mobileNav [data-page="sale"]').click()
 mobile.screenshot(path=str(root/'tests'/'v2-mobile-sale.png'),full_page=True)
 assert not mobile.evaluate('document.documentElement.scrollWidth>window.innerWidth')
 mobile.locator('#mobileNav [data-page="coop"]').click()
 mobile.screenshot(path=str(root/'tests'/'v2-mobile-coop.png'),full_page=True)
 assert not mobile.evaluate('document.documentElement.scrollWidth>window.innerWidth')
 assert mobile.locator('#mobileNav button').count()==9
 assert mobile.locator('#mobileNav [data-action="more"]').count()==0
 assert mobile.evaluate('document.querySelector("#mobileNav").scrollWidth > document.querySelector("#mobileNav").clientWidth')
 mobile.locator('#mobileNav [data-page="settings"]').click()
 assert mobile.locator('#crumb').inner_text()=='Settings'
 mobile.locator('#mobileNav [data-page="weekly"]').click()
 assert mobile.locator('#crumb').inner_text()=='Weekly Tracker'
 print('errors',errors)
 assert not errors,errors
 browser.close()
