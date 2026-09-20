from pathlib import Path


class SchedulerTab:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config

    def render(self):
        return Path('scheduler_tab.py')
