import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging(events):
    Path('logs').mkdir(exist_ok=True); logger=logging.getLogger('web_automation_bot'); logger.setLevel(logging.INFO); logger.handlers.clear()
    handler=RotatingFileHandler('logs/bot.log',maxBytes=2000000,backupCount=3,encoding='utf-8'); handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s','%H:%M:%S')); logger.addHandler(handler)
    class Adapter:
        def _put(self,level,msg): getattr(logger,level.lower())(msg); events.put((level.upper(),msg))
        def info(self,msg): self._put('info',msg)
        def warning(self,msg): self._put('warning',msg)
        def error(self,msg): self._put('error',msg)
    return Adapter()
