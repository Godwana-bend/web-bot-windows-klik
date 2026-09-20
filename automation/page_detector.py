import asyncio
import time


class PageDetector:
    def __init__(self, page, clicker, config, emit, stop_event, pause_event):
        self.page = page
        self.clicker = clicker
        self.config = config
        self.emit = emit
        self.stop_event = stop_event
        self.pause_event = pause_event
        self.last_trigger = 0.0

    async def run(self):
        detection_cfg = self.config.get('detection', {})
        cooldown_seconds = float(detection_cfg.get('cooldown_seconds', 5))
        selector = detection_cfg.get('selector', '')
        expected = detection_cfg.get('expected_text', '')
        detection_type = detection_cfg.get('type', 'element_appears')

        queue = asyncio.Queue()

        async def notify(payload):
            await queue.put(payload)

        await self.page.expose_function('__wab_notify', notify)
        await self.page.evaluate(
            """
            ({ selector, detection_type, expected }) => {
                const root = document.body || document.documentElement;
                if (window.__wab_observer) {
                    window.__wab_observer.disconnect();
                }

                const getText = () => {
                    const node = selector ? document.querySelector(selector) : document.body;
                    if (!node) {
                        return '';
                    }
                    const text = node.innerText || node.textContent || '';
                    return String(text).trim();
                };

                const report = () => {
                    const el = selector ? document.querySelector(selector) : null;
                    const payload = {
                        hasElement: !!el,
                        visible: !!(el && (el.offsetWidth || el.offsetHeight || el.getClientRects().length)),
                        enabled: !!(el && !el.disabled),
                        text: getText(),
                        url: location.href,
                        detectionType: detection_type,
                    };
                    window.__wab_notify(payload);
                };

                window.__wab_observer = new MutationObserver(() => report());
                window.__wab_observer.observe(root, {
                    childList: true,
                    subtree: true,
                    attributes: true,
                    characterData: true,
                    attributeFilter: ['disabled', 'class', 'style', 'aria-disabled', 'data-status'],
                });
                report();
            }
            """,
            {'selector': selector, 'detection_type': detection_type, 'expected': expected},
        )

        while not self.stop_event.is_set():
            try:
                payload = await asyncio.wait_for(queue.get(), timeout=0.5)
            except asyncio.TimeoutError:
                continue

            if self.pause_event.is_set() is False:
                continue

            if detection_type == 'element_appears':
                if not payload.get('hasElement'):
                    continue
            elif detection_type == 'element_becomes_visible':
                if not payload.get('visible'):
                    continue
            elif detection_type == 'element_becomes_enabled':
                if not payload.get('enabled'):
                    continue
            elif detection_type == 'text_appears':
                if expected.lower() not in str(payload.get('text', '')).lower():
                    continue
            elif detection_type == 'text_changes':
                if payload.get('text', '') == '':
                    continue
            elif detection_type == 'url_changes':
                if not payload.get('url'):
                    continue

            now = time.monotonic()
            if now - self.last_trigger < cooldown_seconds:
                continue

            try:
                await self.clicker.click_selector()
                self.last_trigger = now
                self.emit.info('Detection trigger fired')
            except Exception as exc:  # pragma: no cover - runtime branch
                self.emit.error(f'Detection click failed: {exc}')
