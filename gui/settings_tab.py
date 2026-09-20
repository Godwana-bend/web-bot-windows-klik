from pathlib import Path


class SettingsTab:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config

    def render(self):
        return Path('settings_tab.py')
