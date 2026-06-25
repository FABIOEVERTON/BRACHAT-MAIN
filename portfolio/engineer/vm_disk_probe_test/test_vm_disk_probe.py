import os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vm_disk_probe_test import get_usage, gb

class Test(unittest.TestCase):
    def test_gb(self):
        self.assertAlmostEqual(gb(1073741824), 1.0, 5)
    def test_usage_keys(self):
        d = get_usage()
        for k in ("t","u","f","p"): self.assertIn(k, d)
        self.assertIsInstance(d["p"], int)
        self.assertGreaterEqual(d["p"], 0)
        self.assertLessEqual(d["p"], 100)

if __name__ == "__main__":
    unittest.main()
