from pathlib import Path


class LogPanel:
    def __init__(self, parent):
        self.parent = parent

    def render(self):
        return Path('log_panel.py')
