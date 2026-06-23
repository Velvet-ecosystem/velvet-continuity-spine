# SPDX-License-Identifier: GPL-3.0-only

import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "velvet_continuity"


class Python38SyntaxTests(unittest.TestCase):
    def test_all_package_modules_parse_as_python38(self):
        failures = []
        for path in sorted(PACKAGE.glob("*.py")):
            source = path.read_text(encoding="utf-8")
            try:
                ast.parse(source, filename=str(path), feature_version=8)
            except SyntaxError as exc:
                failures.append("{}:{}:{}".format(path.name, exc.lineno, exc.msg))
        self.assertEqual(failures, [], "Python 3.8 syntax failures: {}".format(failures))


if __name__ == "__main__":
    unittest.main()
