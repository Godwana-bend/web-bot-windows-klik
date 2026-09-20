import asyncio
from datetime import datetime, timedelta


class ManualRefreshMonitor:
    """Refreshes at a conservative interval and alerts the user when a target is ready.

    This monitor intentionally never clicks. It is designed for human-in-the-loop use.
    """

    def __init__(self, page, clicker, config, emit, stop_event, pause_event):
        self.page = page
        self.clicker = clicker
        self.config = config
        self.emit = emit
        self.stop_event = stop_event
        self.pause_event = pause_event
        self.last_ready = False

    async def _wait_for_start(self, start_time):
        if not start_time or start_time == 'now':
            return
        try:
            target = datetime.combine(
                datetime.now().date(),
                datetime.strptime(start_time, '%H:%M:%S').time(),
            )
            if target < datetime.now():
                target += timedelta(days=1)
            await asyncio.sleep(max(0, (target - datetime.now()).total_seconds()))
        except ValueError:
            self.emit.warning('Invalid start time. Starting immediately.')

    async def _target_status(self):
        selector_type = self.config.get('selector_type', 'css')
        selector = self.config.get('selector', '')
        if not selector:
            return False, 'Target selector is empty.'

        timeout_ms = int(self.config.get('browser', {}).get('timeout_ms', 10000))
        locator = self.clicker.locator_for(selector_type, selector)
        try:
            await locator.wait_for(state='attached', timeout=min(timeout_ms, 3000))
            visible = await locator.is_visible()
            enabled = await locator.is_enabled()
            if visible and enabled:
                return True, 'Target is visible and enabled.'
            if visible:
                return False, 'Target is visible but disabled.'
            return False, 'Target exists but is not visible.'
        except Exception as exc:
            return False, f'Target is not ready: {exc}'

    async def run(self):
        refresh_cfg = self.config.get('refresh', {})
        interval_seconds = max(5.0, float(refresh_cfg.get('interval_seconds', 10)))
        start_time = self.config.get('schedule', {}).get('start_time', 'now')
        await self._wait_for_start(start_time)
        self.emit.info(
            f'Manual monitor started. Refresh interval: {interval_seconds:g}s. '
            'Automatic clicking is disabled.'
        )

        while not self.stop_event.is_set():
            while not self.pause_event.is_set() and not self.stop_event.is_set():
                await asyncio.sleep(0.1)
            if self.stop_event.is_set():
                break

            try:
                await self.page.reload(
                    wait_until='domcontentloaded',
                    timeout=int(self.config.get('browser', {}).get('timeout_ms', 10000)),
                )
                ready, detail = await self._target_status()
                if ready and not self.last_ready:
                    self.emit.info(
                        'TARGET READY: the button is active. Please click it manually in the browser.'
                    )
                    try:
                        import winsound
                        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                    except (ImportError, RuntimeError):
                        pass
                elif not ready:
                    self.emit.info(detail)
                self.last_ready = ready
            except Exception as exc:
                self.emit.warning(f'Refresh/check failed: {exc}')

            await asyncio.sleep(interval_seconds)
