import json
import re

import pytest
from playwright.sync_api import expect
from tests.helpers.common_test_setup_assertions import validate_shop_page


@pytest.fixture()
def get_products():
    with open('data/products.json') as f:  # path is relative to project root
        products = json.load(f)['products']
        return products


@pytest.mark.feature("BUILD_CART")
@pytest.mark.build_shopping_cart
def test_build_shopping_cart(page_instance, logger_utility, get_products):
    shop_page = validate_shop_page(page_instance, logger_utility, get_products)

    # assert that all items from get_products fixture exist in the shop page
    # if a product exists, add it to cart

    cart = dict()

    for product in get_products:
        product_name = product['product_name']
        shop_page_product = shop_page.inventory_product_names.filter(
            has_text=re.compile(rf"\b{re.escape(product_name)}\b")
        )
        try:
            logger_utility.info(f'shop page product count: {shop_page_product.count()}')
            expect(shop_page_product).to_have_count(1)
            logger_utility.info(f"{product['product_name']} found")
            cart[product_name] = shop_page.add_product_to_cart(product_name)
        except AssertionError:
            logger_utility.error(
                f"Shop page does not have this product: {product['product_name']}"
            )
            raise

    logger_utility.info(f'Shopping cart details: {cart}')

    # open the cart page

    cart_page = shop_page.open_cart()

    # verify number on cart icon matches number of items in the cart and the dictionary

    cart_size = len(cart)
    logger_utility.info(f' Size of shopping cart: {cart_size}')
    cart_icon_size = int(cart_page.cart_icon.inner_text())

    try:
        expect(cart_page.cart_icon).to_have_text(str(cart_size))
        logger_utility.info(f'Shopping cart size matches shopping cart icon: {cart_size}')
    except AssertionError:
        logger_utility.error(f'Shopping cart size: {cart_size} does not match shopping cart icon: {cart_icon_size}')
        raise

    try:
        expect(cart_page.cart_items).to_have_count(cart_size)
        logger_utility.info(f'Shopping cart size matches shopping cart items on the page: {cart_size}')
    except AssertionError:
        logger_utility.error(f'Shopping cart size: {cart_size} does not match shopping cart items length on the cart '
                             f'page: {cart_icon_size}')
        raise

    # verify continue shopping and checkout buttons exist

    try:
        expect(cart_page.continue_shopping_button).to_be_visible()
        logger_utility.info('Continue shopping button is visible')
    except AssertionError:
        logger_utility.error('Continue shopping button not visible')
        raise

    try:
        expect(cart_page.checkout_button).to_be_visible()
        logger_utility.info('Checkout button is visible')
    except AssertionError:
        logger_utility.error('Checkout button not visible')
        raise

    # verify each item's details compared to the cart dictionary and also verify visibility of Remove button for each
    # item

    cart_page_product_dict = dict()

    items = cart_page.cart_items
    items_count = items.count()

    for i in range(items_count):
        item = items.nth(i)
        product_name = item.locator('.inventory_item_name').inner_text().strip()
        product_description = item.locator('.inventory_item_desc').inner_text().strip()
        product_price = item.locator('.inventory_item_price').inner_text().strip()
        cart_page_product_dict[product_name] = {'description': product_description,
                                                'price': product_price}
        remove_button = item.locator('button')
        try:
            expect(remove_button).to_be_visible()
            logger_utility.info('Remove button is visible')
        except AssertionError:
            logger_utility.error('Remove button is not visible')
            raise

    logger_utility.info(f'Shopping cart stored in dictionary: {cart}')
    logger_utility.info(f'Shopping cart displayed on cart page: {cart_page_product_dict}')

    try:
        assert cart_page_product_dict == cart, 'Shopping cart details do not match'
        logger_utility.info('Shopping cart details match')
    except AssertionError:
        logger_utility.error('Shopping cart details do not match')
        raise
