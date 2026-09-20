from pathlib import Path


class DetectorTab:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config

    def render(self):
        return Path('detector_tab.py')
