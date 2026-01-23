from page_objects.cart import CartPage
from page_objects.shop import ShopPage
from page_objects.login import LoginPage
from page_objects.product import ProductPage
from page_objects.checkout_step1 import CheckoutStep1
from page_objects.checkout_step2 import CheckoutStep2
import tests.helpers.test_assertions as test_assertions
from tests.conftest import logger_utility
from tools.scenario_context import ScenarioContext


def run_spec(page, spec):
    context = ScenarioContext()

    for block in spec["flow"]:
        if "steps" in block:
            for step in block["steps"]:
                execute_step(page, step, context)

        if "assertions" in block:
            for assertion in block["assertions"]:
                execute_assertion(page, assertion, context)


def execute_step(page, step, context):
    action = step["action"]
    params = step.get("parameters", {})

    if action == "login":
        login_page = LoginPage(page)
        login_page.login(user_name=params["user_name"],
                         password=params["password"])

    elif action == "add_to_cart":
        shop_page = ShopPage(page)
        products = step["parameters"].get("products", [])
        for product in products:
            shop_page.add_product_to_cart(product)
            logger_utility().info(f'Attempting to add {product} to shopping cart')

    elif action == "open_cart":
        shop = ShopPage(page)
        shop.open_cart()

    elif action == "remove_product_from_cart":
        logger_utility().info(f'Attempting to remove {params["product_name"]} from shopping cart')
        cart = CartPage(page)
        cart.remove_product_from_cart(params["product_name"])

    elif action == "open_product":
        product = params["product_name"]
        logger_utility().info(f'{product} attempted to be viewed')
        shop_page = ShopPage(page)
        shop_page.open_product(product_to_view=params["product_name"])

    elif step["action"] == "capture_product_details":
        shop_page = ShopPage(page)
        details = shop_page.get_product_details(
            step["parameters"]["product_name"]
        )
        # get a dictionary of the product to view and return it and set it to the scenario context
        context.set(step["parameters"]["save_as"], details)

    elif step["action"] == "capture_cart_details":
        cart_page = CartPage(page)
        cart_details = cart_page.get_cart_details()
        # get a list of dictionaries of the shopping cart items
        context.set(step["parameters"]["save_as"], cart_details)

    elif action == "click_checkout":
        cart_page = CartPage(page)
        cart_page.checkout()
        logger_utility().info('Checkout Step 1 page loaded')

    elif action == "fill_user_info":
        checkout_step1_page = CheckoutStep1(page)
        checkout_step1_page.fill_personal_details()

    elif action == "continue_checkout":
        checkout_step1_page = CheckoutStep1(page)
        checkout_step1_page.continue_checkout()
        logger_utility().info('Checkout Step 2 page loaded')

    elif action == "finish_checkout":
        checkout_step2_page = CheckoutStep2(page)
        checkout_step2_page.finish_checkout()
        logger_utility().info('Finish checkout page loaded')

    else:
        raise ValueError(f"Unknown action: {action}")


def execute_assertion(page, assertion, context):
    if "login_page_loaded" in assertion:
        for item in assertion["login_page_loaded"]:
            test_assertions.assert_login_page_loaded(page, item)
    elif "shop_page_loaded" in assertion:
        for item in assertion["shop_page_loaded"]:
            test_assertions.assert_shop_page_loaded_after_login(page, item)

    elif "login_error" in assertion:
        for item in assertion["login_error"]:
            test_assertions.execute_invalid_login_assertions(page, item)

    elif "cart_contains" in assertion:
        for item in assertion["cart_contains"]:
            test_assertions.assert_cart_contains(page, item)

    elif "product_page_loaded" in assertion:
        for item in assertion["product_page_loaded"]:
            test_assertions.execute_product_detail_assertion(page, item)

    elif "product_details" in assertion:
        for item in assertion["product_details"]:
            test_assertions.execute_product_detail_assertion(page, item)

    elif "cart_details_after_removing_product" in assertion:
        for item in assertion["cart_details_after_removing_product"]:
            test_assertions.execute_cart_assertions(page, item)

    elif "cart_badge_icon" in assertion:
        for item in assertion["cart_badge_icon"]:
            test_assertions.execute_cart_assertions(page, item)

    elif "cart_page" in assertion:
        for item in assertion["cart_page"]:
            test_assertions.execute_cart_assertions(page, item)

    elif "product_details_match" in assertion:
        product_page = ProductPage(page)
        expected = context.get(
            assertion["product_details_match"]["context_key"]
        )

        actual = product_page.get_product_details()

        try:
            assert actual == expected, (f'Product details do not between inventory page and product page '
                                        f'Expected: {expected} / Actual: {actual}')
            logger_utility().info(f'Product details match between inventory page and product page '
                                  f'Expected: {expected} / Actual: {actual}')
        except AssertionError:
            logger_utility().error(f'Product details do not between inventory page and product page '
                                   f'Expected: {expected} / Actual: {actual}')
            raise


    elif "checkout_step1_loaded" in assertion:
        for item in assertion["checkout_step1_loaded"]:
            test_assertions.execute_checkout_step1_assertions(page, item)

    elif "checkout_step2_loaded" in assertion:
        for item in assertion["checkout_step2_loaded"]:
            test_assertions.execute_checkout_step2_assertions(page, item)

    elif "checkout_step2_financials" in assertion:
        for item in assertion["checkout_step2_financials"]:
            test_assertions.execute_checkout_step2_assertions(page, item)

    elif "checkout_complete_loaded" in assertion:
        for item in assertion["checkout_complete_loaded"]:
            test_assertions.execute_finish_checkout_assertions(page, item)

    elif "cart_details_match" in assertion:
        checkout_step2_page = CheckoutStep2(page)
        expected = context.get(
            assertion["cart_details_match"]["context_key"]
        )

        actual = checkout_step2_page.get_checkout_items()

        try:
            assert actual == expected, (f'Shopping cart details do not match between cart page and checkout step 2 page '
                                        f'Expected: {expected} / Actual: {actual}')
            logger_utility().info(f'Shopping cart details match between cart page and checkout step 2 page '
                                  f'Expected: {expected} / Actual: {actual}')
        except AssertionError:
            logger_utility().error(f'Shopping cart details do not match between cart page and checkout step 2 page '
                                   f'Expected: {expected} / Actual: {actual}')
            raise

    else:
        raise ValueError(f"Unknown assertion type: {assertion}")
