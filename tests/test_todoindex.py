import os
import tempfile
import unittest

from todoindex import scan, to_markdown


class TodoTest(unittest.TestCase):
    def test_scan(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "x.py")
            open(path, "w").write("# TODO: later\nx = 1\n# FIXME now\n")
            rows = list(scan(tmp))
            self.assertEqual([r[2] for r in rows], ["TODO", "FIXME"])

    def test_markdown(self):
        self.assertIn("| File |", to_markdown([]))


if __name__ == "__main__":
    unittest.main()
