Pre-Req:

pip install rich pytest-rerunfailures
pip install pytest-html

From project root:

python run_tests.py

Using a marker:

python run_tests.py -m smoke

Using rerun failures feature:

python run_tests.py --rerun-failed -m smoke

