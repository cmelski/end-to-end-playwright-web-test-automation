# tools/feature_coverage.py
import json
from pathlib import Path

OUTPUT = Path("reports/feature_coverage.json")


def pytest_collection_modifyitems(items):
    features = set()

    for item in items:
        for mark in item.iter_markers(name="feature"):
            features.add(mark.args[0])

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(sorted(features), indent=2))

# After pytest runs, you’ll have:

# reports/feature_coverage.json
