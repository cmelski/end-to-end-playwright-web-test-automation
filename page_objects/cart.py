class CartPage:

    def __init__(self, page):
        self.page = page
        self.cart_icon = self.page.locator('.shopping_cart_badge')
        self.cart_items = self.page.locator('.cart_item')
        self.checkout_button = self.page.locator('#checkout')
        self.continue_shopping_button = self.page.locator('#continue-shopping')

