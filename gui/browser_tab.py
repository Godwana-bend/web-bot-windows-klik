from pathlib import Path


class BrowserTab:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config

    def render(self):
        return Path('browser_tab.py')
