from __future__ import annotations

import json
import os
import glob


def test_fixture_json_integrity():
    """Ensure all active JSON fixture files parse cleanly (no trailing concatenated data)."""
    fixtures_dir = os.path.join(os.path.dirname(__file__), "..", "fixtures")
    fixtures_dir = os.path.abspath(fixtures_dir)
    if not os.path.isdir(fixtures_dir):
        return
    problems = []
    for path in glob.glob(os.path.join(fixtures_dir, "*.json")):
        # Skip disabled/backup fixtures
        if path.endswith('.bak'):
            continue
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            json.loads(content)
        except Exception as e:  # noqa: BLE001
            problems.append(f"{os.path.basename(path)}: {e}")
    assert not problems, "Invalid JSON fixture files: \n" + "\n".join(problems)
