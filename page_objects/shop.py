from page_objects.product import ProductPage


class ShopPage:

    def __init__(self, page):
        self.page = page
        self.url = self.page.url
        self.title = self.page.locator('.title')
        self.inventory_items = self.page.locator('.inventory_item')

    def get_product_info(self, product_to_view):
        product = self.inventory_items.filter(has_text=product_to_view)
        product.locator('a').first.click()
        product_page = ProductPage(self.page)
        return product_page
