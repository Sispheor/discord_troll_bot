import unittest
from datetime import datetime

from utils import get_played_session_minute


class TestUtils(unittest.TestCase):

    def test_get_played_session_minute(self):
        # datetime(year, month, day, hour, minute, second, microsecond)
        date_start = datetime(2021, 11, 1, 21, 00, 00, 0)
        date_end = datetime(2021, 11, 1, 21, 30, 00, 0)
        self.assertEqual(get_played_session_minute(date_start, date_end), 30)

