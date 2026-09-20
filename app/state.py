from dataclasses import dataclass
from enum import Enum


class AutomationState(str, Enum):
    IDLE = 'IDLE'
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    STOPPING = 'STOPPING'
    STOPPED = 'STOPPED'
    ERROR = 'ERROR'


@dataclass
class AppState:
    state: AutomationState = AutomationState.IDLE
    browser_open: bool = False
    url: str = 'https://example.com'
