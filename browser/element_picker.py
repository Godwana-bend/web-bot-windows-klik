from .selector_engine import best_selector
class ElementPicker:
    async def install(self,page,callback):
        await page.expose_function('__wab_pick',callback)
        await page.evaluate("""() => { document.addEventListener('click',e=>{const n=e.target;e.preventDefault();e.stopPropagation();window.__wab_pick({tag:n.tagName,id:n.id,name:n.getAttribute('name'),'aria-label':n.getAttribute('aria-label'),role:n.getAttribute('role'),text:(n.innerText||'').trim(),data-testid:n.getAttribute('data-testid')})},true) }""")
