# tools/check_feature_coverage.py
import yaml, json
from pathlib import Path

features_file = Path("features/features.yaml")
coverage_file = Path("reports/feature_coverage.json")

defined = set(yaml.safe_load(features_file.read_text())["features"].keys())
covered = set(json.loads(coverage_file.read_text()))

missing = defined - covered

print(f"\nFeature coverage: {len(covered)}/{len(defined)}")

if missing:
    print("\nMissing coverage:")
    for f in sorted(missing):
        print(f" - {f}")
    raise SystemExit(1)
