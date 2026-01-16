class ProductPage:

    def __init__(self, page):
        self.page = page
        self.product_name = self.page.locator('div[data-test="inventory-item-name"]').inner_text()
