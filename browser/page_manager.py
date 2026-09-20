class PageManager:
    def __init__(self, page):
        self.page = page

    async def get_url(self):
        return self.page.url
