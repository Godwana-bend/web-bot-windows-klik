from pathlib import Path
from playwright.async_api import async_playwright
class BrowserManager:
    def __init__(self,cfg,emit): self.cfg=cfg; self.emit=emit; self.pw=None; self.context=None; self.page=None
    async def start(self):
        self.pw=await async_playwright().start(); profile=Path('profiles/default'); profile.mkdir(parents=True,exist_ok=True)
        b=self.cfg.get('browser',{}); self.context=await self.pw.chromium.launch_persistent_context(str(profile),headless=bool(b.get('headless',False)),viewport=None)
        self.page=self.context.pages[0] if self.context.pages else await self.context.new_page(); self.emit.info('Browser started')
    async def open(self,url):
        if url: await self.page.goto(url,wait_until='domcontentloaded',timeout=self.cfg.get('browser',{}).get('timeout_ms',10000))
        self.emit.info('Page loaded'); return self.page
    async def close(self):
        if self.context: await self.context.close()
        if self.pw: await self.pw.stop()
