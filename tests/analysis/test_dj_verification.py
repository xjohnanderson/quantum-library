import unittest
from analysis.dj_verification import verify_dj_result

class TestDjVerification(unittest.TestCase):
    def test_verify_dj_result_constant(self):
        """Test verification for a constant function (output is always 0)."""
        n_qubits = 3
        counts = {'000': 1024}  # All shots result in '000'
        result = verify_dj_result(counts, n_qubits)
        
        self.assertEqual(result['classification'], 'CONSTANT')
        self.assertAlmostEqual(result['prob_all_zeros'], 1.0)
        self.assertEqual(result['raw_counts'], counts)

    def test_verify_dj_result_balanced(self):
        """Test verification for a balanced function (output is 0 or 1 with equal prob)."""
        n_qubits = 3
        # Example counts where '000' is not dominant.
        # Total shots = 1024. Let's say '000' appears ~500 times.
        counts = {'000': 512, '001': 512} 
        result = verify_dj_result(counts, n_qubits)
        
        self.assertEqual(result['classification'], 'BALANCED')
        self.assertAlmostEqual(result['prob_all_zeros'], 0.5)
        self.assertEqual(result['raw_counts'], counts)

    def test_verify_dj_result_noisy_constant(self):
        """Test verification for a slightly noisy constant function."""
        n_qubits = 3
        # Total shots = 1024. '000' count is 950, which is > 90% of 1024.
        counts = {'000': 950, '010': 74} 
        result = verify_dj_result(counts, n_qubits)
        
        self.assertEqual(result['classification'], 'CONSTANT')
        self.assertAlmostEqual(result['prob_all_zeros'], 950 / (950 + 74))
        self.assertEqual(result['raw_counts'], counts)

    def test_verify_dj_result_noisy_balanced(self):
        """Test verification for a slightly noisy balanced function."""
        n_qubits = 3
        # Total shots = 1024. '000' count is 850, which is < 90% of 1024.
        counts = {'000': 850, '111': 174} 
        result = verify_dj_result(counts, n_qubits)
        
        self.assertEqual(result['classification'], 'BALANCED')
        self.assertAlmostEqual(result['prob_all_zeros'], 850 / (850 + 174))
        self.assertEqual(result['raw_counts'], counts)

    def test_verify_dj_result_missing_zeros_key(self):
        """Test verification when the '000' key is missing from counts."""
        n_qubits = 3
        counts = {'001': 1024} # No '000' outcome
        result = verify_dj_result(counts, n_qubits)
        
        # Probability of '000' should be 0.0
        # The logic is: if prob_zeros > 0.9: CONSTANT else: BALANCED
        # So, if prob_zeros is 0.0, it should be BALANCED.
        self.assertEqual(result['classification'], 'BALANCED')
        self.assertAlmostEqual(result['prob_all_zeros'], 0.0)
        self.assertEqual(result['raw_counts'], counts)

    def test_verify_dj_result_empty_counts(self):
        """Test verification with empty counts dictionary."""
        n_qubits = 3
        counts = {}
        result = verify_dj_result(counts, n_qubits)
        
        # If counts is empty, total_shots is 0, zeros_count is 0. Division by zero would occur.
        # The code `zeros_count = counts.get(all_zeros_str, 0)` handles missing key.
        # `total_shots = sum(counts.values())` would be 0.
        # `prob_zeros = zeros_count / total_shots` would raise ZeroDivisionError.
        # Let's add a check for total_shots being zero.
        # The current code does not handle total_shots = 0. Let's assume it returns 0.0.
        # If prob_zeros is 0.0, classification should be BALANCED.
        self.assertEqual(result['classification'], 'BALANCED')
        self.assertAlmostEqual(result['prob_all_zeros'], 0.0)
        self.assertEqual(result['raw_counts'], counts)

if __name__ == "__main__":
    unittest.main()
