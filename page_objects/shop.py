from page_objects.cart import CartPage
from page_objects.product import ProductPage


class ShopPage:

    def __init__(self, page):
        self.page = page
        self.url = self.page.url
        self.title = self.page.locator('.title')
        self.inventory_items = self.page.locator('.inventory_item')
        self.inventory_product_names = self.inventory_items.locator('.inventory_item_name')

    def get_product_info(self, product_to_view):
        product = self.inventory_items.filter(has_text=product_to_view)
        product.locator('a').first.click()
        product_page = ProductPage(self.page)
        return product_page

    def add_product_to_cart(self, product_name):

        # locate the specific product from the inventory by the product parameter

        product_to_add = self.inventory_items.filter(
            has=self.page.locator(".inventory_item_name", has_text=product_name)
        )

        # locate the product description and price

        product_description = product_to_add.locator('.inventory_item_desc').inner_text()
        product_price = product_to_add.locator('.inventory_item_price').inner_text()

        # add these details to a dictionary

        product_dict = {'description': product_description,
                        'price': product_price}

        # find the button for this product and click to add it to cart

        product_to_add.get_by_role("button", name="Add to cart").click()

        # return the dictionary

        return product_dict

    def open_cart(self):
        self.page.locator('.shopping_cart_link').click()
        cart_page = CartPage(self.page)
        return cart_page
