import asyncio
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
class ClickEngine:
    def __init__(self,page,cfg,emit): self.page=page; self.cfg=cfg; self.emit=emit; self.clicks=[]
    def locator(self):
        typ=self.cfg.get('selector_type','css'); s=self.cfg.get('selector','')
        if typ=='xpath': return self.page.locator('xpath='+s)
        if typ=='text': return self.page.get_by_text(s,exact=True).first
        if typ=='role': return self.page.get_by_role(s).first
        if typ in ('aria','aria-label'): return self.page.get_by_label(s).first
        return self.page.locator(s)
    async def click(self):
        if self.page.is_closed(): raise RuntimeError('Page is closed')
        now=__import__('time').monotonic(); self.clicks=[t for t in self.clicks if now-t<60]
        if len(self.clicks)>=int(self.cfg.get('click',{}).get('max_clicks_per_minute',20)): raise RuntimeError('Maximum clicks per minute reached')
        loc=self.locator(); timeout=int(self.cfg.get('browser',{}).get('timeout_ms',10000))
        await loc.wait_for(state='visible',timeout=timeout); await loc.scroll_into_view_if_needed()
        if not await loc.is_enabled(): raise RuntimeError('Target element is disabled')
        await asyncio.sleep(float(self.cfg.get('click',{}).get('delay_ms',100))/1000)
        await loc.click(timeout=timeout); self.clicks.append(now); self.emit.info('Click successful')
    async def click_selector(self): return await self.click()
    async def click_xpath(self): return await self.click()
    async def click_text(self): return await self.click()
    async def click_role(self): return await self.click()
    async def click_coordinate(self,x,y): await self.page.mouse.click(x,y)
