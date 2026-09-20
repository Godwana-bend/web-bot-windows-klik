import asyncio
import threading

from app.state import AutomationState
from automation.click_engine import ClickEngine
from automation.page_detector import PageDetector
from automation.scheduler import Scheduler
from browser.browser_manager import BrowserManager


class AutomationController:
    def __init__(self, config, events, logger, app_state):
        self.config = config
        self.events = events
        self.logger = logger
        self.app_state = app_state
        self.state = AutomationState.IDLE
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.thread = None
        self.loop = None
        self.browser = None

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        self.stop_event.clear()
        self.pause_event.set()
        self.state = AutomationState.RUNNING
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(self._worker())
        except Exception as exc:
            self.state = AutomationState.ERROR
            self.logger.error(f'Automation failed: {exc}')
        finally:
            self.loop.close()
            self.state = AutomationState.STOPPED
            self.app_state.state = self.state

    async def _worker(self):
        self.browser = BrowserManager(self.config, self.logger, self.app_state)
        await self.browser.start()
        url = self.config.get('url', 'https://example.com')
        page = await self.browser.open(url)
        click_engine = ClickEngine(page, self.config, self.logger)

        mode = self.config.get('mode', 'scheduled')
        if mode in ('scheduled', 'hybrid'):
            await Scheduler(click_engine, self.config, self.logger, self.stop_event, self.pause_event).run()
        if mode in ('detection', 'hybrid') and not self.stop_event.is_set():
            await PageDetector(page, click_engine, self.config, self.logger, self.stop_event, self.pause_event).run()

    def pause(self):
        self.pause_event.clear()
        self.state = AutomationState.PAUSED
        self.app_state.state = self.state
        self.logger.info('Automation paused')

    def resume(self):
        self.pause_event.set()
        self.state = AutomationState.RUNNING
        self.app_state.state = self.state
        self.logger.info('Automation resumed')

    def stop(self):
        self.stop_event.set()
        self.pause_event.set()
        self.state = AutomationState.STOPPING
        self.app_state.state = self.state
        self.logger.info('Automation stopping')

    def test_click(self):
        if self.browser and self.browser.page:
            loop = self.loop or asyncio.get_event_loop()
            if loop.is_running():
                asyncio.run_coroutine_threadsafe(self._test_click(), loop)
        else:
            self.logger.error('Browser not started yet')

    async def _test_click(self):
        if self.browser is None or self.browser.page is None:
            self.logger.error('Browser not started')
            return
        try:
            engine = ClickEngine(self.browser.page, self.config, self.logger)
            await engine.test_click()
        except Exception as exc:
            self.logger.error(f'Test click failed: {exc}')
