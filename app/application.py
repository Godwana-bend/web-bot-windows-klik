import queue

import customtkinter as ctk

from app.state import AppState
from automation.automation_controller import AutomationController
from config.config_manager import ConfigManager
from gui.main_window import MainWindow
from utils.logger import setup_logging


class Application:
    def __init__(self):
        self.config = ConfigManager()
        self.config.load()
        self.state = AppState(url=self.config.get('url', 'https://example.com'))
        self.events = queue.Queue()
        self.logger = setup_logging(self.events)
        self.controller = AutomationController(self.config, self.events, self.logger, self.state)

        self.root = ctk.CTk()
        self.root.title('Web Automation Bot')
        self.root.geometry('980x760')
        self.root.minsize(900, 640)
        self.window = MainWindow(self.root, self.config, self.controller, self.state)
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.root.after(120, self._poll_events)

    def _poll_events(self):
        try:
            while True:
                event = self.events.get_nowait()
                self.window.handle_event(event)
        except queue.Empty:
            pass
        self.root.after(120, self._poll_events)

    def run(self):
        self.root.mainloop()

    def close(self):
        self.controller.stop()
        self.root.destroy()
