class ProductPage:

    def __init__(self, page):
        self.page = page
        self.product_name = self.page.locator('div[data-test="inventory-item-name"]').inner_text()
        self.back_to_shop_page = self.page.locator('#back-to-products')
        self.add_to_cart_button = self.page.locator('#add-to-cart')
        self.remove_from_cart_button = self.page.locator('#remove')

    def add_to_cart(self):
        self.add_to_cart_button.click()

