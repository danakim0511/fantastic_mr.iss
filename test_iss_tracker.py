import unittest
from unittest.mock import patch
from io import StringIO
from datetime import datetime, timezone
from iss_tracker import (
    parse_iss_data,
    calculate_average_speed,
    find_closest_data_point,
    print_data_range,
)


class TestISSTracker(unittest.TestCase):
    def setUp(self):
        # Sample XML data for testing
        self.sample_xml_data = {
            "ndm": {
                "oem": {
                    "body": {
                        "segment": {
                            "data": {
                                "stateVector": [
                                    {"EPOCH": "2024-01-01T00:00:00.000Z", "X": {"#text": "1.0"}, "Y": {"#text": "2.0"}, "Z": {"#text": "3.0"}},
                                    {"EPOCH": "2024-01-02T00:00:00.000Z", "X": {"#text": "4.0"}, "Y": {"#text": "5.0"}, "Z": {"#text": "6.0"}},
                                ]
                            }
                        }
                    }
                }
            }
        }

    def test_parse_iss_data(self):
        iss_data = parse_iss_data(self.sample_xml_data)
        self.assertEqual(len(iss_data), 2)
        self.assertEqual(iss_data[0]["EPOCH"], "2024-01-01T00:00:00.000Z")
        self.assertEqual(iss_data[1]["Y"], 5.0)

    def test_calculate_average_speed(self):
        iss_data = [
            {"X_DOT": 1.0, "Y_DOT": 2.0, "Z_DOT": 3.0},
            {"X_DOT": 4.0, "Y_DOT": 5.0, "Z_DOT": 6.0},
        ]
        avg_speed = calculate_average_speed(iss_data)
        expected_avg_speed = 4.115599
        margin_of_error = 5.0
        self.assertLess(abs(avg_speed - expected_avg_speed), margin_of_error)

    def test_find_closest_data_point(self):
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        iss_data = [
            {"EPOCH": "2024-01-01T00:00:00.000Z"},
            {"EPOCH": "2024-01-02T00:00:00.000Z"},
        ]
        # Print the original iss_data for debugging
        print("Original iss_data:", iss_data)
    
        closest_data_point = find_closest_data_point(iss_data)
    
        # Print the sorted iss_data for debugging
        print("Sorted iss_data:", iss_data)
    
        self.assertEqual(closest_data_point["EPOCH"], "2024-01-02T00:00:00.000Z")

    def test_print_data_range(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            iss_data = [
                {"EPOCH": "2024-01-01T00:00:00.000Z"},
                {"EPOCH": "2024-01-02T00:00:00.000Z"},
            ]
            print_data_range(iss_data)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "Data range from 2024-01-01T00:00:00.000Z to 2024-01-02T00:00:00.000Z")


if __name__ == '__main__':
    unittest.main()

