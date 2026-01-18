Smart CLI Runner:

Pre-Req:

pip install rich pytest-rerunfailures
pip install pytest-html

From project root:

python run_tests.py

Using a marker:

python run_tests.py -m smoke

Using rerun failures feature:

python run_tests.py --rerun-failed -m smoke

Feature Coverage Functionality:

-define a features.yaml file
-tag tests with the features: e.g. @pytest.mark.feature("AUTH_LOGIN")
-in conftest.py add this:
from tools.feature_coverage import pytest_collection_modifyitems
-create a feature_coverage.py under tools directory to collect the features that were actually run by your tests
-create a check_feature_coverage.py script to compare youyr features.yaml and the actual feature coverage from the pytest run
-create a generate_feature_dashboard .py script to generate a HTML view of the feature coverage

Steps:
run your tests
python tools/check_feature_coverage.py
python tools/generate_feature_dashboard.py



