import asyncio
import time


class ClickEngine:
    def __init__(self, page, config, emit):
        self.page = page
        self.config = config
        self.emit = emit
        self.click_history = []

    def locator_for(self, selector_type, value):
        if selector_type == 'xpath':
            return self.page.locator(f'xpath={value}')
        if selector_type == 'text':
            return self.page.get_by_text(value, exact=True).first
        if selector_type == 'role':
            return self.page.get_by_role(value).first
        if selector_type in ('aria', 'aria-label'):
            return self.page.get_by_label(value).first
        return self.page.locator(value)

    async def _validate_target(self, locator, timeout_ms):
        if self.page.is_closed():
            raise RuntimeError('Page is closed.')
        await locator.wait_for(state='visible', timeout=timeout_ms)
        await locator.scroll_into_view_if_needed()
        if not await locator.is_enabled():
            raise RuntimeError('Target element is disabled.')

    async def click_selector(self):
        selector_type = self.config.get('selector_type', 'css')
        selector = self.config.get('selector', '')
        return await self._click_with_selector(selector_type, selector)

    async def click_xpath(self, selector):
        return await self._click_with_selector('xpath', selector)

    async def click_text(self, text):
        return await self._click_with_selector('text', text)

    async def click_role(self, role):
        return await self._click_with_selector('role', role)

    async def click_coordinate(self, x, y):
        await self.page.mouse.click(x, y)

    async def _click_with_selector(self, selector_type, value):
        if not value:
            raise RuntimeError('Target selector is empty.')

        timeout_ms = int(self.config.get('browser', {}).get('timeout_ms', 10000))
        locator = self.locator_for(selector_type, value)
        await self._validate_target(locator, timeout_ms)

        current = time.monotonic()
        one_minute_ago = current - 60
        self.click_history = [ts for ts in self.click_history if ts > one_minute_ago]
        max_per_minute = int(self.config.get('click', {}).get('max_clicks_per_minute', 20))
        if len(self.click_history) >= max_per_minute:
            raise RuntimeError('Maximum clicks per minute reached.')

        delay_seconds = float(self.config.get('click', {}).get('delay_ms', 100)) / 1000.0
        if delay_seconds > 0:
            await asyncio.sleep(delay_seconds)

        await locator.click(timeout=timeout_ms)
        self.click_history.append(current)
        self.emit.info('Click successful')

    async def test_click(self):
        try:
            await self.click_selector()
            self.emit.info('Test click successful')
            return True
        except Exception as exc:
            self.emit.error(str(exc))
            return False
