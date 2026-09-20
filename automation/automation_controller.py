import asyncio,threading
from browser.browser_manager import BrowserManager
from automation.click_engine import ClickEngine
from automation.scheduler import Scheduler
from automation.page_detector import PageDetector
from app.state import AutomationState
class AutomationController:
    def __init__(self,cfg,events,logger): self.cfg=cfg; self.events=events; self.logger=logger; self.state=AutomationState.IDLE; self.stop_event=threading.Event(); self.pause_event=threading.Event(); self.pause_event.set(); self.thread=None; self.loop=None; self.browser=None
    def start(self):
        if self.thread and self.thread.is_alive(): return
        self.stop_event.clear(); self.pause_event.set(); self.state=AutomationState.RUNNING; self.thread=threading.Thread(target=self._run,daemon=True); self.thread.start()
    def _run(self):
        self.loop=asyncio.new_event_loop(); asyncio.set_event_loop(self.loop)
        try: self.loop.run_until_complete(self._worker())
        except Exception as exc: self.state=AutomationState.ERROR; self.logger.error(str(exc))
        finally: self.loop.close(); self.state=AutomationState.STOPPED
    async def _worker(self):
        self.browser=BrowserManager(self.cfg,self.logger); await self.browser.start(); page=await self.browser.open(self.cfg.get('url','')); c=ClickEngine(page,self.cfg,self.logger); mode=self.cfg.get('mode','scheduled')
        if mode in ('scheduled','hybrid'): await Scheduler(c,self.cfg,self.logger,self.stop_event,self.pause_event).run()
        if mode in ('detection','hybrid') and not self.stop_event.is_set(): await PageDetector(page,c,self.cfg,self.logger,self.stop_event,self.pause_event).run()
    def pause(self): self.pause_event.clear(); self.state=AutomationState.PAUSED; self.logger.info('Automation paused')
    def resume(self): self.pause_event.set(); self.state=AutomationState.RUNNING; self.logger.info('Automation resumed')
    def stop(self): self.stop_event.set(); self.pause_event.set(); self.state=AutomationState.STOPPING
    def test_click(self):
        if self.loop and self.loop.is_running(): asyncio.run_coroutine_threadsafe(self.browser_test(),self.loop)
    async def browser_test(self):
        try: await ClickEngine(self.browser.page,self.cfg,self.logger).click(); self.logger.info('Test click successful')
        except Exception as exc: self.logger.error('Test click failed: '+str(exc))
