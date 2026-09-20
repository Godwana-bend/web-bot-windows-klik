import json
from pathlib import Path

DEFAULT = {
    'url': 'https://example.com',
    'selector_type': 'css',
    'selector': '#submit-button',
    'mode': 'manual',
    'schedule': {
        'start_time': 'now',
        'interval_seconds': 30,
        'click_count': 1,
        'repeat_until_stopped': False,
    },
    'refresh': {
        'interval_seconds': 10,
        'notify_only': True,
    },
    'detection': {
        'type': 'element_appears',
        'selector': '#available-button',
        'expected_text': 'Available',
        'cooldown_seconds': 5,
    },
    'browser': {
        'headless': False,
        'timeout_ms': 10000,
    },
    'click': {
        'delay_ms': 100,
        'max_clicks_per_minute': 20,
    },
}


class ConfigManager:
    def __init__(self, path='config.json'):
        self.path = Path(path)
        self.data = {}

    def load(self):
        try:
            self.data = json.loads(self.path.read_text(encoding='utf-8'))
            self._deep_merge(self.data, DEFAULT)
        except (OSError, json.JSONDecodeError):
            self.data = json.loads(json.dumps(DEFAULT))
            self.save()
        return self.data

    def save(self):
        self.path.write_text(json.dumps(self.data, indent=2), encoding='utf-8')

    def reset(self):
        self.data = json.loads(json.dumps(DEFAULT))
        self.save()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value

    def _deep_merge(self, target, source):
        for key, value in source.items():
            if isinstance(value, dict):
                target.setdefault(key, {})
                self._deep_merge(target[key], value)
            else:
                target.setdefault(key, value)
