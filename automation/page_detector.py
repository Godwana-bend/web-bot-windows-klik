import asyncio
OBSERVER="""(selector,type,expected,notify)=>{if(window.__wab_observer)window.__wab_observer.disconnect();let last='';const check=()=>{let value=type==='url'?location.href:Array.from(selector?document.querySelectorAll(selector):[document.body]).map(n=>JSON.stringify({text:n.innerText||'',visible:!!(n.offsetWidth||n.offsetHeight||n.getClientRects().length),enabled:!n.disabled,attrs:[n.className,n.getAttribute('aria-disabled'),n.getAttribute('data-status')]})).join('|');if(value!==last){last=value;notify({value,url:location.href})}};window.__wab_observer=new MutationObserver(check);window.__wab_observer.observe(document.documentElement,{childList:true,subtree:true,attributes:true,characterData:true});check()}"""
class PageDetector:
    def __init__(self,page,clicker,cfg,emit,stop,pause): self.page=page; self.c=clicker; self.cfg=cfg; self.emit=emit; self.stop=stop; self.pause=pause; self.last=0
    async def run(self):
        d=self.cfg.get('detection',{}); typ=d.get('type','element_appears'); expected=d.get('expected_text',''); cooldown=float(d.get('cooldown_seconds',5)); q=asyncio.Queue()
        await self.page.expose_function('__wab_notify',lambda data:q.put_nowait(data)); await self.page.evaluate(OBSERVER,d.get('selector',''),typ,expected,'__wab_notify')
        while not self.stop.is_set():
            try: data=await asyncio.wait_for(q.get(),.5)
            except asyncio.TimeoutError: continue
            if not self.pause.is_set(): continue
            if typ in ('text_appears','text_changes') and expected.lower() not in data.get('value','').lower(): continue
            now=__import__('time').monotonic()
            if now-self.last<cooldown: continue
            try: await self.c.click(); self.last=now
            except Exception as exc: self.emit.error('Detection click failed: '+str(exc))
