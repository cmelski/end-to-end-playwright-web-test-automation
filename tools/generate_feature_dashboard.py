
import json
import yaml
from pathlib import Path

FEATURES_FILE = Path("features/features.yaml")
COVERAGE_FILE = Path("reports/feature_coverage.json")
OUTPUT_FILE = Path("reports/feature_coverage.html")

defined = yaml.safe_load(FEATURES_FILE.read_text())["features"]
covered = set(json.loads(COVERAGE_FILE.read_text()))

rows = []
for feature, meta in defined.items():
    status = "covered" if feature in covered else "missing"
    rows.append(
        f"""
        <tr class="{status}">
            <td>{feature}</td>
            <td>{meta.get('description', '')}</td>
            <td>{'✅' if status == 'covered' else '❌'}</td>
        </tr>
        """
    )

coverage_percent = int((len(covered) / len(defined)) * 100)

html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Feature Coverage Report</title>
<style>
    body {{
        font-family: system-ui, sans-serif;
        background: #0f172a;
        color: #e5e7eb;
        padding: 2rem;
    }}
    h1 {{
        margin-bottom: 0.5rem;
    }}
    .summary {{
        margin-bottom: 1.5rem;
        font-size: 1.1rem;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        background: #020617;
    }}
    th, td {{
        padding: 0.75rem;
        border-bottom: 1px solid #1f2933;
        text-align: left;
    }}
    th {{
        background: #020617;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.08em;
    }}
    tr.covered {{
        background: rgba(20, 184, 166, 0.1);
    }}
    tr.missing {{
        background: rgba(239, 68, 68, 0.1);
    }}
</style>
</head>
<body>

<h1>Feature Coverage Dashboard</h1>
<div class="summary">
    Coverage: <strong>{len(covered)} / {len(defined)}</strong>
    ({coverage_percent}%)
</div>

<table>
    <thead>
        <tr>
            <th>Feature</th>
            <th>Description</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        {''.join(rows)}
    </tbody>
</table>

</body>
</html>
"""

OUTPUT_FILE.parent.mkdir(exist_ok=True)
OUTPUT_FILE.write_text(html)

print(f"Feature coverage dashboard generated: {OUTPUT_FILE}")
