import json
import time

import pytest
from playwright.sync_api import expect
from page_objects.shop import ShopPage
import re


@pytest.fixture()
def get_products():
    with open('data/products.json') as f:  # path is relative to project root
        products = json.load(f)['products']
        return products


@pytest.mark.smoke
@pytest.mark.view_product_info
def test_view_product_info_page(page_instance, logger_utility, get_products):
    logger_utility.info(get_products)
    shop_page = ShopPage(page_instance)
    logger_utility.info(f'Shop URL: {shop_page.url}')
    logger_utility.info(f'Successfully bypassed Login screen for this test')
    # The following line can’t work because shop_page.url is a string, not a Playwright object
    # and expect() in Playwright only works with Page, Locator, or APIResponse objects.
    # expect(shop_page.url).to_contain_text('inventory')
    # do this instead (3 ways):
    # simplest(no waiting)
    assert "inventory.html" in shop_page.page.url
    logger_utility.info('"inventory.html" exists in the url')
    # exact url match (less flexible)
    expect(shop_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
    logger_utility.info('Page correctly has url: https://www.saucedemo.com/inventory.html')
    # more flexible (reg ex)
    expect(shop_page.page).to_have_url(re.compile(r"/inventory\.html$"))
    logger_utility.info('URL contains "inventory"')

    # assert there are items to select and fail the test and log the error to test_failures.log
    try:
        expect(shop_page.inventory_items).not_to_have_count(0)
    except AssertionError:
        logger_utility.error("Inventory count is 0. Test Failed", exc_info=True)
        raise

    inventory_count = shop_page.inventory_items.count()
    logger_utility.info(f'Shop Page Inventory Count: {inventory_count}')

    # select a product from the inventory; use products.json to get product name

    product_to_view = get_products[0]['product_name']

    # In Playwright Python, the best way is not to manually loop unless you truly need to.
    # Playwright gives you locator filtering that is cleaner, faster, and auto-waiting.

    product_page = shop_page.get_product_info(product_to_view)
    try:
        assert product_page.product_name == product_to_view
        logger_utility.info(f'Selected product {product_page.product_name} matches product on View Products page: {product_to_view}')
    except AssertionError:
        logger_utility.error(f'Selected product {product_page.product_name} does not match product on View Products page: {product_to_view}. Test Failed')
        raise

    # assert Back to Products link exists

    try:
        expect(product_page.back_to_shop_page).to_be_visible()
        logger_utility.info('Back to products link exists')
    except AssertionError:
        logger_utility.error(f'Back to products link does not exist. Test Failed')
        raise

    # assert Add to cart or Remove button exists

    try:
        if product_page.add_to_cart_button.is_visible():
            logger_utility.info("Add to cart button exists")
            product_page.add_to_cart()
            expect(product_page.remove_from_cart_button).to_be_visible()
            logger_utility.info("Remove button exists after clicking Add to Cart")
        else:
            logger_utility.info("Product already in cart")
            expect(product_page.remove_from_cart_button).to_be_visible()
    except AssertionError:
        logger_utility.error('Add to cart and Remove button do not exist. Test failed')
        raise

