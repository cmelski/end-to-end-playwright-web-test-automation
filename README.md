AI-Driven Test Automation Framework (Python + Playwright)

This project is a Python Playwright test automation framework designed to demonstrate modern test engineering practices, including AI-assisted test specification generation, feature coverage tracking, and a clean separation of concerns using Page Object Models (POM), YAML feature specs, and data-driven testing.

The goal of this framework is to show how AI can assist test creation and coverage analysis without sacrificing test clarity and maintainability.

Key Concepts & Design Goals

Readable, reviewable test intent (YAML specs instead of hard-coded flows)

No assertions in Page Objects (strict POM discipline)

Feature-level coverage visibility

AI used as a generator, not a black box

Scalable for real-world test suites

Technology Stack

Python

Playwright (Python)

pytest

YAML (test specifications)

JSON (test data)

Custom Python tooling for feature coverage & reporting

LLM-assisted spec generation (optional step)

## 📁 Project Structure (High Level)

```text
data/                      # JSON test data
features/                  # YAML feature definitions
├── generated/             # AI-generated feature specs
page_objects/              # Page Object Models (locators & actions only)
reports/                   # Feature coverage HTML reports
test_run_logs/             # Test logs (errors, exceptions, runtime info)
tests/                     # pytest entry points and conftest.py
├── helpers/               # Assertion helpers (Playwright expect lives here)
tools/                     # Framework utilities and scripts
├── ai_generate_specs.py   # Generate feature specs via LLM prompts
├── feature_coverage.py    # Compile executed features from pytest markers
├── check_feature_coverage.py # Compare defined vs executed features
├── generate_feature_dashboard.py # Generate HTML feature coverage dashboard
├── spec_runner.py         # Execute steps defined in YAML feature specs
└── utils.py               # Shared helpers (env vars, parsing, etc.)
```
            
Page Object Model (POM) Design

Page Objects only contain locators and user actions

No assertions inside POMs

Assertions are executed via:

YAML feature specs

Centralized assertion handlers

This keeps:

Page Objects reusable

Assertions consistent

Tests easy to reason about

YAML Feature Specifications

Test intent is defined in YAML, not Python.

Example:

feature: BUILD_CART
scenario: Add products to cart
steps:
  - action: login
    parameters:
      user: $USER
      password: $PASSWORD
  - action: add_to_cart
    parameters:
      product_name: ${PRODUCT_1}
assertions:
  - product_details:
      selector: "button[data-test='remove']"
      toBeVisible: true

Why YAML?

Easy to review in PRs

Easy for AI to generate

Decouples what we test from how we test it

Data-Driven Testing

Test data lives in JSON files

YAML specs reference data using environment variables or data keys

Enables:

Multiple scenarios from the same spec

Cleaner test logic

No hard-coded values in test code

Feature Tagging & Test Execution Flow
1️⃣ Feature Tagging

Each pytest test is tagged with a feature marker, for example:

@pytest.mark.feature("BUILD_CART")
def test_build_cart_from_spec():
    ...


These markers are the foundation for feature coverage tracking.

2️⃣ Run the Test Suite
pytest


Tests execute via Playwright

YAML specs are interpreted by the spec runner

Assertions are validated using Playwright expect

3️⃣ Generate Feature Coverage Data

After test execution:

python tools/feature_coverage.py


This produces a JSON file listing which features were exercised by the test suite.

4️⃣ Validate Coverage Against Defined Features
python tools/check_feature_coverage.py


This compares:

Features defined in features.yaml

Features actually covered by tests

This step highlights missing or untested features.

5️⃣ Generate Feature Coverage Dashboard
python tools/generate_feature_dashboard.py


This produces a visual dashboard/report showing:

Covered features

Missing features

Overall feature coverage status

## Feature Coverage Dashboard

![Feature coverage dashboard](images/feature_dashboard.png)



AI-Driven Spec Generation (Optional, Assisted Step)

AI is used to:

Generate initial YAML feature specs

Suggest test steps and assertions based on feature descriptions

Important:

Generated specs are reviewed and refined by humans

AI does not execute tests or make runtime decisions

This keeps the framework transparent and auditable

The AI accelerates test authoring — it does not replace test engineering judgment.

Why This Approach?

This framework demonstrates:

How AI can be integrated responsibly into test automation

How to keep tests maintainable as suites grow

How to measure feature coverage, not just code coverage

How to design automation that scales beyond demo projects


