import asyncio
from datetime import datetime,timedelta
class Scheduler:
    def __init__(self,clicker,cfg,emit,stop_event,pause_event): self.c=clicker; self.cfg=cfg; self.emit=emit; self.stop=stop_event; self.pause=pause_event
    async def run(self):
        s=self.cfg.get('schedule',{}); interval=max(.1,float(s.get('interval_seconds',30))); count=int(s.get('click_count',1)); repeat=bool(s.get('repeat_until_stopped',False)); start=s.get('start_time','now')
        if start!='now':
            try:
                target=datetime.combine(datetime.now().date(),datetime.strptime(start,'%H:%M:%S').time())
                if target<datetime.now(): target+=timedelta(days=1)
                await asyncio.sleep(max(0,(target-datetime.now()).total_seconds()))
            except ValueError: self.emit.warning('Invalid start time; starting immediately')
        done=0
        while not self.stop.is_set() and (repeat or done<count):
            while not self.pause.is_set() and not self.stop.is_set(): await asyncio.sleep(.1)
            if self.stop.is_set(): break
            try: await self.c.click(); done+=1
            except Exception as exc: self.emit.error('Click failed: '+str(exc))
            await asyncio.sleep(interval)
