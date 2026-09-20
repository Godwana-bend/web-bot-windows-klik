import asyncio
from datetime import datetime, timedelta


class Scheduler:
    def __init__(self, clicker, config, emit, stop_event, pause_event):
        self.clicker = clicker
        self.config = config
        self.emit = emit
        self.stop_event = stop_event
        self.pause_event = pause_event

    async def run(self):
        schedule = self.config.get('schedule', {})
        interval_seconds = max(0.1, float(schedule.get('interval_seconds', 30)))
        click_count = int(schedule.get('click_count', 1))
        repeat_until_stopped = bool(schedule.get('repeat_until_stopped', False))
        start_time = schedule.get('start_time', 'now')

        if start_time and start_time != 'now':
            try:
                target = datetime.combine(datetime.now().date(), datetime.strptime(start_time, '%H:%M:%S').time())
                if target < datetime.now():
                    target += timedelta(days=1)
                wait_seconds = max(0, (target - datetime.now()).total_seconds())
                await asyncio.sleep(wait_seconds)
            except ValueError:
                self.emit.warning('Invalid start time. Starting immediately.')

        completed = 0
        while not self.stop_event.is_set() and (repeat_until_stopped or completed < click_count):
            while self.pause_event.is_set() is False and not self.stop_event.is_set():
                await asyncio.sleep(0.1)
            if self.stop_event.is_set():
                break
            try:
                await self.clicker.click_selector()
                completed += 1
                self.emit.info(f'Scheduler click #{completed} succeeded')
            except Exception as exc:  # pragma: no cover - runtime path
                self.emit.error(f'Scheduler click failed: {exc}')
            if not repeat_until_stopped and completed >= click_count:
                break
            await asyncio.sleep(interval_seconds)
