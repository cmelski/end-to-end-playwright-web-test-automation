class CheckoutStep1:

    def __init__(self, page):
        self.page = page
        self.title = self.page.locator('.title')
        self.first_name = self.page.locator('#first-name')
        self.last_name = self.page.locator('#last-name')
        self.postal_code = self.page.locator('#postal-code')
        self.continue_checkout_process_button = self.page.locator('#continue')
        self.cancel_button = self.page.locator('#cancel')

    def fill_personal_details(self):
        self.first_name.fill('Chris')
        self.last_name.fill('Melski')
        self.postal_code.fill('234567')

    def continue_checkout(self):
        self.continue_checkout_process_button.click()

    def cancel_checkout(self):
        self.cancel_button.click()