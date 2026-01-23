
class CartPage:

    def __init__(self, page):
        self.page = page
        self.cart_icon = self.page.locator('.shopping_cart_badge')
        self.cart_items = self.page.locator('.cart_item')
        self.checkout_button = self.page.locator('#checkout')
        self.continue_shopping_button = self.page.locator('#continue-shopping')

    def remove_product_from_cart(self, product):
        items = self.cart_items
        items_count = items.count()

        for i in range(items_count):
            item = items.nth(i)
            product_name = item.locator('.inventory_item_name').inner_text().strip()
            if product_name == product:
                remove_button = item.locator('button')
                remove_button.click()

    def get_cart_details(self):
        cart_details_list = []
        cart = self.cart_items
        cart_item_count = cart.count()

        for i in range(cart_item_count):
            item = cart.nth(i)
            product_name = item.locator('.inventory_item_name').inner_text().strip()
            product_description = item.locator('.inventory_item_desc').inner_text().strip()
            product_price = item.locator('.inventory_item_price').inner_text().strip()
            product_quantity = item.locator('.cart_quantity').inner_text().strip()
            cart_details = {"name": product_name,
                            "price": product_price,
                            "description": product_description,
                            "quantity": product_quantity,

                            }
            cart_details_list.append(cart_details)

        return cart_details_list

    def checkout(self):
        self.checkout_button.click()
