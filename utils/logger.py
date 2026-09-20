import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(events):
    Path('logs').mkdir(exist_ok=True)
    logger = logging.getLogger('web_automation_bot')
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    handler = RotatingFileHandler('logs/bot.log', maxBytes=2_000_000, backupCount=3, encoding='utf-8')
    handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%H:%M:%S'))
    logger.addHandler(handler)

    class Adapter:
        def info(self, message):
            logger.info(message)
            events.put(('INFO', message))

        def warning(self, message):
            logger.warning(message)
            events.put(('WARNING', message))

        def error(self, message):
            logger.error(message)
            events.put(('ERROR', message))

    return Adapter()
