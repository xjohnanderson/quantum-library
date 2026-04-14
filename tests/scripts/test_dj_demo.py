# tests/test_dj_demo.py

import unittest
from unittest.mock import patch
import io
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from scripts.dj_demo import run_demo


class TestDjDemoScript(unittest.TestCase):

    @patch('utils.visualization.show_quantum_object', return_value=None)
    def test_dj_demo_outputs(self, mock_show):
        """Test that dj_demo.py produces the expected output strings for both cases."""
        # Capture ALL printed output in one go
        captured = io.StringIO()
        with patch('sys.stdout', new=captured):
            run_demo()

        output = captured.getvalue()

        # Check constant_0 case
        self.assertIn("DEMO: CONSTANT_0 CASE", output)
        self.assertIn("Detected Function Type: CONSTANT", output)

        # Check balanced case
        self.assertIn("DEMO: BALANCED CASE", output)
        self.assertIn("Detected Function Type: BALANCED", output)

        # General checks
        self.assertIn("Probability of |000>:", output)
        self.assertIn("Measurement Counts:", output)
        self.assertIn("000", output)   # constant case
        self.assertIn("111", output)   # balanced case (all 1s for n=3)


if __name__ == "__main__":
    unittest.main(verbosity=2)