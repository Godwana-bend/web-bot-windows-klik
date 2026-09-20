from browser.selector_engine import best_selector


class ElementPicker:
    def __init__(self):
        self._active = False

    async def install(self, page, callback):
        self._active = True
        await page.expose_function('__wab_pick', callback)
        await page.evaluate(
            """
            () => {
                const overlay = document.createElement('div');
                overlay.style.position = 'fixed';
                overlay.style.pointerEvents = 'none';
                overlay.style.border = '2px solid #3b82f6';
                overlay.style.background = 'rgba(59,130,246,0.14)';
                overlay.style.zIndex = '2147483646';
                overlay.style.display = 'none';
                document.body.appendChild(overlay);

                const onMove = (event) => {
                    const el = event.target;
                    const rect = el.getBoundingClientRect();
                    overlay.style.display = 'block';
                    overlay.style.left = `${Math.round(rect.left)}px`;
                    overlay.style.top = `${Math.round(rect.top)}px`;
                    overlay.style.width = `${Math.max(Math.round(rect.width), 8)}px`;
                    overlay.style.height = `${Math.max(Math.round(rect.height), 8)}px`;
                };

                document.addEventListener('mousemove', onMove, true);
                document.addEventListener('click', (event) => {
                    const el = event.target;
                    event.preventDefault();
                    event.stopPropagation();
                    const data = {
                        tag: el.tagName,
                        id: el.id,
                        class: el.className,
                        name: el.getAttribute('name'),
                        'aria-label': el.getAttribute('aria-label'),
                        role: el.getAttribute('role'),
                        text: (el.innerText || '').trim(),
                        'data-testid': el.getAttribute('data-testid'),
                    };
                    overlay.style.display = 'none';
                    window.__wab_pick(data);
                }, true);
            }
            """
        )

    def active(self):
        return self._active
