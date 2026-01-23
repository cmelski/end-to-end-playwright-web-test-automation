class FinishCheckout:

    def __init__(self, page):
        self.page = page
        self.title = self.page.locator('.title')
        self.finish_checkout_icon = self.page.locator('.pony_express')
