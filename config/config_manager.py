import json
from pathlib import Path
DEFAULT={'url':'https://example.com','selector_type':'css','selector':'','mode':'scheduled','schedule':{'start_time':'now','interval_seconds':30,'click_count':10,'repeat_until_stopped':False},'detection':{'type':'element_appears','selector':'','expected_text':'','cooldown_seconds':5},'browser':{'headless':False,'timeout_ms':10000},'click':{'delay_ms':100,'max_clicks_per_minute':20}}
class ConfigManager:
    def __init__(self,path='config.json'): self.path=Path(path); self.data={}
    def load(self):
        try: self.data=json.loads(self.path.read_text(encoding='utf-8')); self._merge(DEFAULT)
        except (OSError,json.JSONDecodeError): self.data=json.loads(json.dumps(DEFAULT))
        return self.data
    def _merge(self,src):
        for k,v in src.items():
            if isinstance(v,dict): self.data.setdefault(k,{}); self._merge_dict(self.data[k],v)
            else: self.data.setdefault(k,v)
    @staticmethod
    def _merge_dict(dst,src):
        for k,v in src.items(): dst.setdefault(k,json.loads(json.dumps(v)) if isinstance(v,dict) else v)
    def save(self): self.path.write_text(json.dumps(self.data,indent=2),encoding='utf-8')
    def reset(self): self.data=json.loads(json.dumps(DEFAULT)); self.save()
    def get(self,key,default=None): return self.data.get(key,default)
