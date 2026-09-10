from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
 page.goto('https://moko.by/',wait_until='domcontentloaded');page.wait_for_function("!document.title.includes('One moment')",timeout=45000);page.wait_for_timeout(2500)
 print(page.title());page.screenshot(path='/home/user/moko/site_screenshot.png',full_page=True)
 open('/home/user/moko/site_loaded.html','w').write(page.content())
 print(page.evaluate("JSON.stringify({fonts: [...new Set([...document.querySelectorAll('h1,h2,p,a')].map(e=>getComputedStyle(e).fontFamily))],images:[...document.images].map(e=>e.src),styles:[...document.querySelectorAll('link[rel=stylesheet]')].map(e=>e.href)})"))
 b.close()
