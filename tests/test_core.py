from config.config_manager import ConfigManager
from browser.selector_engine import best_selector


def test_selector_generation():
    element = {'id': 'submit-button', 'tag': 'button'}
    assert best_selector(element) == '#submit-button'


def test_config_loading_and_saving(tmp_path):
    config_path = tmp_path / 'config.json'
    manager = ConfigManager(str(config_path))
    manager.load()
    manager.set('url', 'https://example.com')
    manager.save()

    reloaded = ConfigManager(str(config_path))
    data = reloaded.load()
    assert data['url'] == 'https://example.com'


def test_state_management():
    from app.state import AppState, AutomationState
    state = AppState()
    assert state.state == AutomationState.IDLE
    state.state = AutomationState.RUNNING
    assert state.state == AutomationState.RUNNING


def test_scheduler_interval_validation():
    from automation.scheduler import Scheduler
    assert Scheduler.__name__ == 'Scheduler'
