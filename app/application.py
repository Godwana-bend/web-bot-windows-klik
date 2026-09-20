import queue
import customtkinter as ctk
from app.state import AppState
from config.config_manager import ConfigManager
from automation.automation_controller import AutomationController
from gui.main_window import MainWindow
from utils.logger import setup_logging

class Application:
    def __init__(self):
        self.events=queue.Queue(); self.state=AppState(); self.config=ConfigManager(); self.config.load()
        self.logger=setup_logging(self.events)
        self.controller=AutomationController(self.config,self.events,self.logger)
        self.root=ctk.CTk(); self.window=MainWindow(self.root,self.config,self.controller,self.state)
        self.root.protocol('WM_DELETE_WINDOW',self.close); self.root.after(100,self._drain)
    def _drain(self):
        while True:
            try: self.window.handle_event(self.events.get_nowait())
            except queue.Empty: break
        self.root.after(100,self._drain)
    def run(self): self.root.mainloop()
    def close(self): self.controller.stop(); self.root.destroy()
