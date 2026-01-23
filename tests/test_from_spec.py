import json
import yaml
import pytest
from tools.spec_runner import execute_step, execute_assertion
from tools.utils import substitute_env_vars, replace_placeholders
from tests.conftest import logger_utility
from tools.scenario_context import ScenarioContext


@pytest.fixture()
def get_products():
    with open('data/products.json') as f:  # path is relative to project root
        products = json.load(f)['products']
        return products


@pytest.mark.feature("AUTH_LOGIN")
def test_valid_login(page_instance_login):
    with open("features/generated/auth_login.yaml") as f:
        spec = yaml.safe_load(f)
    spec = substitute_env_vars(spec)
    logger_utility().info(f'YAML auth_login feature file loaded: {spec} ')

    context = ScenarioContext()

    # Loop over flow, which may contain steps or assertions
    for block in spec["flow"]:
        if "steps" in block:
            for step in block["steps"]:
                execute_step(page_instance_login, step, context)
        elif "assertions" in block:
            for assertion in block["assertions"]:
                execute_assertion(page_instance_login, assertion, context)


@pytest.mark.feature("INVALID_LOGIN")
def test_invalid_login(page_instance_login):
    # Load YAML
    with open("features/generated/invalid_login.yaml") as f:
        spec = yaml.safe_load(f)

    spec = substitute_env_vars(spec)
    spec = replace_placeholders(spec)
    logger_utility().info(f'YAML invalid_login feature file loaded: {spec}')

    context = ScenarioContext()

    # Loop over flow, which may contain steps or assertions
    for block in spec["flow"]:
        if "steps" in block:
            for step in block["steps"]:
                execute_step(page_instance_login, step, context)
        elif "assertions" in block:
            for assertion in block["assertions"]:
                execute_assertion(page_instance_login, assertion, context)


@pytest.mark.feature("VIEW_PRODUCT")
def test_view_product(page_instance):
    with open("features/generated/view_product.yaml") as f:
        spec = yaml.safe_load(f)
    spec = substitute_env_vars(spec)
    spec = replace_placeholders(spec)
    logger_utility().info(f'YAML view feature file loaded: {spec} ')

    context = ScenarioContext()

    # Loop over flow, which may contain steps or assertions
    for block in spec["flow"]:
        if "steps" in block:
            for step in block["steps"]:
                execute_step(page_instance, step, context)
        elif "assertions" in block:
            for assertion in block["assertions"]:
                execute_assertion(page_instance, assertion, context)
@pytest.mark.feature("BUILD_CART")
def test_build_cart(page_instance):
    with open("features/generated/build_cart.yaml") as f:
        spec = yaml.safe_load(f)
    spec = substitute_env_vars(spec)
    spec = replace_placeholders(spec)
    logger_utility().info(f'YAML build_cart feature file loaded: {spec} ')

    context = ScenarioContext()

    for step in spec["steps"]:
        execute_step(page_instance, step, context)

    for assertion in spec["assertions"]:
        execute_assertion(page_instance, assertion, context)



@pytest.mark.feature("CART_REMOVE_ITEM")
def test_remove_product_from_cart(page_instance, get_products):
    # Load YAML
    with open("features/generated/cart_remove_item.yaml") as f:
        spec = yaml.safe_load(f)

    spec = substitute_env_vars(spec)
    spec = replace_placeholders(spec)
    logger_utility().info(f'YAML cart_remove_item feature file loaded: {spec}')

    context = ScenarioContext()

    # Loop over flow, which may contain steps or assertions
    for block in spec["flow"]:
        if "steps" in block:
            for step in block["steps"]:
                execute_step(page_instance, step, context)
        elif "assertions" in block:
            for assertion in block["assertions"]:
                execute_assertion(page_instance, assertion, context)

@pytest.mark.feature("CHECKOUT_COMPLETE")
def test_complete_checkout(page_instance):
    with open("features/generated/checkout_complete.yaml") as f:
        spec = yaml.safe_load(f)
    spec = substitute_env_vars(spec)
    spec = replace_placeholders(spec)
    logger_utility().info(f'YAML checkout_complete feature file loaded: {spec} ')

    context = ScenarioContext()

    # Loop over flow, which may contain steps or assertions
    for block in spec["flow"]:
        if "steps" in block:
            for step in block["steps"]:
                execute_step(page_instance, step, context)
        elif "assertions" in block:
            for assertion in block["assertions"]:
                execute_assertion(page_instance, assertion, context)