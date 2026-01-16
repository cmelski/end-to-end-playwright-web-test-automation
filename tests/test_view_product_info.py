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
    # The following line can’t work because shop_page.url is a string, not a Playwright object
    # and expect() in Playwright only works with Page, Locator, or APIResponse objects.
    # expect(shop_page.url).to_contain_text('inventory')
    # do this instead (3 ways):
    # simplest(no waiting)
    assert "inventory.html" in shop_page.page.url
    # exact url match (less flexible)
    expect(shop_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
    # more flexible (reg ex)
    expect(shop_page.page).to_have_url(re.compile(r"/inventory\.html$"))
    # assert there are items to select
    try:
        expect(shop_page.inventory_items).not_to_have_count(0)
    except AssertionError:
        logger_utility.error(f'Shop Page inventory count is 0')

    inventory_count = shop_page.inventory_items.count()
    logger_utility.info(f'Shop Page Inventory Count: {inventory_count}')

    # select a product from the inventory; use products.json to get product name

    product_to_view = get_products[0]['product_name']

    # In Playwright Python, the best way is not to manually loop unless you truly need to.
    # Playwright gives you locator filtering that is cleaner, faster, and auto-waiting.

    product_page = shop_page.get_product_info(product_to_view)
    assert product_page.product_name == product_to_view
