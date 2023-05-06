import unittest
from unittest.mock import MagicMock
from trading_core.handler import HandlerBase, HandlerCurrencyCom
from trading_core.model import Config

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.config = Config()

    def test_getHandler_returns_handler(self):
        handler = self.config.getHandler()
        self.assertIsInstance(handler, HandlerBase)
    
    def test_get_handler(self):
        self.assertIsInstance(self.config.getHandler(), HandlerCurrencyCom)

    def test_getIntervals_returns_list_of_intervals(self):
        intervals = self.config.getIntervals()
        expected_intervals = ['5m', '15m', '30m', '1h', '4h', '1d', '1w']
        self.assertEqual(intervals, expected_intervals)

    def test_get_intervals(self):
        self.assertEqual(self.config.getIntervals(), ["5m", "15m", "30m", "1h", "4h", "1d", "1w"])
        self.assertEqual(self.config.getIntervals(importance='LOW'), ["5m", "15m"])
        self.assertEqual(self.config.getIntervals(importance='MEDIUM'), ["30m", "1h"])
        self.assertEqual(self.config.getIntervals(importance='HIGH'), ["4h", "1d", "1w"])

    def test_get_interval_details(self):
        intervals = self.config.getIntervalDetails()
        self.assertEqual(len(intervals), 7)
        self.assertEqual(intervals[0]["interval"], "5m")
        self.assertEqual(intervals[0]["name"], "5 minutes")
        self.assertEqual(intervals[0]["order"], 10)
        self.assertEqual(intervals[0]["importance"], "LOW")
        self.assertEqual(intervals[1]["interval"], "15m")
        self.assertEqual(intervals[1]["name"], "15 minutes")
        self.assertEqual(intervals[1]["order"], 20)
        self.assertEqual(intervals[1]["importance"], "LOW")

    def test_is_trading_open(self):
        trading_time = 'UTC; Mon 01:05 - 19:00; Tue 01:05 - 19:00; Wed 01:05 - 19:00; Thu 01:05 - 19:00; Fri 01:05 - 19:00'
        trading_timeframe = 'UTC; Mon 01:05 - 19:00; Tue 01:05 - 19:00; Wed 01:05 - 19:00; Thu 01:05 - 19:00; Fri 01:05 - 19:00'
        self.config._Config__tradingTimeframes[trading_time] = MagicMock()
        self.config._Config__tradingTimeframes[trading_time].isTradingOpen.return_value = True
        self.assertTrue(self.config.isTradingOpen(trading_timeframe))

if __name__ == '__main__':
    unittest.main()