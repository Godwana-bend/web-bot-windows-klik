class PageManager:
    def __init__(self,page): self.page=page
    async def url(self): return self.page.url
