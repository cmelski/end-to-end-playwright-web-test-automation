class CheckoutStep2:

    def __init__(self, page):
        self.page = page
        self.title = self.page.locator('.title')
        self.checkout_items = self.page.locator('.cart_item')
        self.subtotal_price = self.page.locator('div[data-test="subtotal-label"]')
        self.tax = self.page.locator('div[data-test="tax-label"]')
        self.total_price = self.page.locator('div[data-test="total-label"]')
        self.finish_button = self.page.locator('#finish')
        self.cancel_button = self.page.locator('#cancel')

    def get_checkout_items(self):
        checkout_items_list = []
        checkout_items = self.checkout_items
        checkout_items_count = checkout_items.count()

        for i in range(checkout_items_count):
            item = checkout_items.nth(i)
            product_name = item.locator('.inventory_item_name').inner_text().strip()
            product_description = item.locator('.inventory_item_desc').inner_text().strip()
            product_price = item.locator('.inventory_item_price').inner_text().strip()
            product_quantity = item.locator('.cart_quantity').inner_text().strip()
            checkout_item_details = {"name": product_name,
                            "price": product_price,
                            "description": product_description,
                            "quantity": product_quantity,

                            }
            checkout_items_list.append(checkout_item_details)

        return checkout_items_list

    def get_subtotal_price(self):

        subtotal_text = self.subtotal_price.inner_text().strip()
        subtotal_price = float(subtotal_text.split('$')[1])
        return subtotal_price

    def get_tax(self):

        tax_text = self.tax.inner_text().strip()
        tax = float(tax_text.split('$')[1])
        return tax

    def get_total_price(self):

        total_price_text = self.total_price.inner_text().strip()
        total_price = float(total_price_text.split('$')[1])
        return total_price

    def get_cart_items_total_price(self):
        checkout_items = self.checkout_items
        checkout_items_count = checkout_items.count()
        checkout_items_subtotal = 0

        for i in range(checkout_items_count):
            item = checkout_items.nth(i)
            product_price_text = item.locator('.inventory_item_price').inner_text().strip()
            product_price = float(product_price_text.split('$')[1])
            checkout_items_subtotal += product_price

        return checkout_items_subtotal

    def finish_checkout(self):
        self.finish_button.click()


