import unittest
from Miniproject import calculate_energy_financials


class TestEnergyFinancials(unittest.TestCase):

    # Case 1: Không đạt mức chiết khấu
    def test_no_discount(self):
        devices = [
            {
                "id": "M01",
                "location": "Workshop A",
                "old_index": 1000,
                "new_index": 11000,
                "status": "Normal"
            }
        ]

        self.assertEqual(
            calculate_energy_financials(devices),
            (10000, 0, 30000000)
        )

    # Case 2: Đúng ngưỡng 50.000 kWh
    def test_discount_threshold(self):
        devices = [
            {
                "id": "M01",
                "location": "Workshop A",
                "old_index": 0,
                "new_index": 50000,
                "status": "Normal"
            }
        ]

        self.assertEqual(
            calculate_energy_financials(devices),
            (50000, 3, 145500000)
        )

    # Case 3: Vượt ngưỡng 50.000 kWh
    def test_discount_above_threshold(self):
        devices = [
            {
                "id": "M01",
                "location": "Workshop A",
                "old_index": 0,
                "new_index": 60000,
                "status": "Normal"
            }
        ]

        self.assertEqual(
            calculate_energy_financials(devices),
            (60000, 3, 174600000)
        )


if __name__ == "__main__":
    unittest.main()