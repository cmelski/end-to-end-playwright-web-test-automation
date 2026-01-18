import os
import logging
import shutil
from pathlib import Path

import pytest

# load test.env file variables
from dotenv import load_dotenv

from playwright.sync_api import sync_playwright, TimeoutError, expect

from tools.feature_coverage import pytest_collection_modifyitems



# define test run parameters
# in terminal you can run for e.g. 'pytest test_web_framework_api.py --browser_name firefox'
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )

    parser.addoption(
        "--url_start", action="store", default="test", help="starting url"
    )

    parser.addoption(
        "--env", action="store", default="test", help="Environment to run tests against")


@pytest.fixture(scope="session")
def env(request):
    env_name = request.config.getoption("--env")
    # Load the corresponding .env file
    load_dotenv(f"{env_name}.env")
    return env_name


@pytest.fixture(scope="session")
def url_start(env):  # env fixture ensures .env is loaded first
    return os.environ.get("BASE_URL")


@pytest.fixture(scope="session")
def valid_login_credentials(env):  # env fixture ensures .env is loaded first
    valid_username = os.environ.get("VALID_USERNAME")
    valid_password = os.environ.get("VALID_PASSWORD")
    valid_credentials = {'user_name': valid_username,
                         'password': valid_password
                         }
    return valid_credentials


@pytest.fixture
def invalid_login_credentials(request, valid_login_credentials):
    if request.param == "empty":
        return "", ""

    if request.param == "bad_password":
        return valid_login_credentials["user_name"], "bad_password"

    if request.param == "bad_username":
        return "bad_username", valid_login_credentials["password"]

    raise ValueError(f"Unknown param: {request.param}")


@pytest.fixture(scope="session")
def logger_utility():
    # set up logging
    logger = logging.getLogger(__name__)
    return logger


# fixture to log in to the website behind the scenes in headless mode
# to produce a session auth state file to be called by page fixture to bypass login screen
@pytest.fixture(scope="function")
def auth_state_file(env, valid_login_credentials):
    path = Path("auth_state_test.json")

    if path.exists():
        return str(path)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.saucedemo.com")

        page.fill("#user-name", valid_login_credentials['user_name'])
        page.fill("#password", valid_login_credentials['password'])
        page.click("#login-button")

        # 🔑 CRITICAL WAIT
        page.wait_for_url("**/inventory.html")
        page.wait_for_selector(".inventory_item")

        # Now cookies + storage exist
        context.storage_state(path=path)

        context.close()
        browser.close()

    return str(path)


# main tests fixture that yields page object
# and then closes context and browser after yield as part of teardown
# this fixture will use an auth_state_file returned by auth_state_file fixture
# to allow bypass of the login screen
@pytest.fixture(scope="function")
def page_instance(request, logger_utility, auth_state_file):
    browser_name = request.config.getoption("browser_name")

    with sync_playwright() as p:
        browser = (
            p.chromium.launch(headless=False)
            if browser_name == "chrome"
            else p.firefox.launch(headless=False)
        )

        context = browser.new_context(storage_state=auth_state_file)
        page = context.new_page()
        page.goto("https://www.saucedemo.com/inventory.html")

        try:
            yield page

        finally:
            context.close()
            browser.close()

            file_path = Path(__file__).parent.parent / "auth_state_test.json"
            if os.path.exists(file_path):
                os.remove(file_path)
                logger_utility.info("Deleted auth_state_test.json.")


# main tests fixture that yields page object
# and then closes context and browser after yield as part of teardown
# this fixture is used for login tests
@pytest.fixture(scope="function")
def page_instance_login(request, url_start):
    browser_name = request.config.getoption("browser_name")

    with sync_playwright() as p:
        if browser_name == "chrome":
            browser = p.chromium.launch(headless=False)
        elif browser_name == "firefox":
            browser = p.firefox.launch(headless=False)

        context = browser.new_context()

        page = context.new_page()

        page.goto(url_start)

        try:
            yield page
        finally:
            context.close()
            browser.close()
