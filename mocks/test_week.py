import unittest
from weekday import get_holidays, requests
from requests.exceptions import Timeout
from unittest.mock import patch


class TestCalendar(unittest.TestCase):
	def test_get_holidays(self):
		with patch.object(requests, "get", side_effect=requests.exceptions.Timeout) as mock_requests:
			mock_requests.get.side_effect = Timeout
			with self.assertRaises(Timeout):
				get_holidays()
				mock_requests.get.assert_called_once()

if __name__ == "__main__":
	unittest.main()

