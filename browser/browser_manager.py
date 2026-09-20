import json
from pathlib import Path

from playwright.async_api import async_playwright


class BrowserManager:
    def __init__(self, config, emit, state=None):
        self.config = config
        self.emit = emit
        self.state = state
        self.pw = None
        self.context = None
        self.page = None

    async def start(self):
        self.pw = await async_playwright().start()
        profile_dir = Path('profiles/default')
        profile_dir.mkdir(parents=True, exist_ok=True)

        browser_cfg = self.config.get('browser', {})
        self.context = await self.pw.chromium.launch_persistent_context(
            str(profile_dir),
            headless=bool(browser_cfg.get('headless', False)),
            viewport={'width': 1280, 'height': 900},
        )
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        self.emit.info('Browser started')
        if self.state is not None:
            self.state.browser_open = True

    async def open(self, url):
        if url:
            timeout = int(self.config.get('browser', {}).get('timeout_ms', 10000))
            await self.page.goto(url, wait_until='domcontentloaded', timeout=timeout)
        self.emit.info('Page loaded')
        return self.page

    async def close(self):
        if self.context:
            await self.context.close()
        if self.pw:
            await self.pw.stop()
        if self.state is not None:
            self.state.browser_open = False
