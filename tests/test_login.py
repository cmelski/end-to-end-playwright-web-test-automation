import pytest
from page_objects.login import LoginPage
from playwright.sync_api import expect


@pytest.mark.feature("AUTH_LOGIN")
@pytest.mark.login
def test_valid_login(page_instance_login, valid_login_credentials, logger_utility):
    login_page = LoginPage(page_instance_login)

    # validate user is on Login Page
    expect(login_page.login_button).to_be_visible()
    logger_utility.info("Login page successfully loaded")

    # perform login
    valid_username = valid_login_credentials["user_name"]
    valid_password = valid_login_credentials["password"]
    shop_page = login_page.valid_login(valid_username, valid_password)

    # assert shop page title
    expect(shop_page.title).to_have_text("Products")
    logger_utility.info("Login successful, Shop page loaded")


@pytest.mark.feature("INVALID_LOGIN")
@pytest.mark.parametrize(
    "invalid_login_credentials",
    ["empty", "bad_password", "bad_username"],
    indirect=True,
)
@pytest.mark.invalid_login
def test_invalid_login(page_instance_login, invalid_login_credentials, logger_utility):
    username, password = invalid_login_credentials
    login_page = LoginPage(page_instance_login)

    # validate user is on Login Page
    expect(login_page.login_button).to_be_visible()
    logger_utility.info("Login page successfully loaded")

    # attempt login
    login_page.invalid_login(username, password)

    # assert invalid login error
    expect(login_page.login_error).to_contain_text("Epic sadface")
    logger_utility.info('Login attempt failed with incorrect user_name and password.')
