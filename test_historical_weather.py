#!/usr/bin/env python
import unittest
import json

from historical_weather import WeatherReport


def format_json(result):
    return json.dumps(result, indent=4)


class TestHistoricalWeather(unittest.TestCase):

    def setUp(self):
        self.wr = WeatherReport('data/test_data.csv')

    def test_simple_max_temp_delta(self):
        args = {
            "function_name": "max-temp-delta",
            "city": "bos",
            "month": None,
            "year": None
        }
        self.wr.set_args(MockArgs(args))
        expected = {
            "city": "bos",
            "date": "2010-01-05",
            "temp_change": 40.0
        }
        self.assertEqual(format_json(expected), self.wr.max_temp_delta())

    def test_max_temp_delta_filter_year(self):
        args = {
            "function_name": "max-temp-delta",
            "city": "bos",
            "month": None,
            "year": 2017
        }
        self.wr.set_args(MockArgs(args))
        expected = {
            "city": "bos",
            "date": "2017-07-15",
            "temp_change": 9.0
        }
        self.assertEqual(format_json(expected), self.wr.max_temp_delta())

    def test_max_temp_delta_filter_month(self):
        args = {
            "function_name": "max-temp-delta",
            "city": "bos",
            "month": 3,
            "year": 2013
        }
        self.wr.set_args(MockArgs(args))
        expected = {
            "city": "bos",
            "date": "2013-03-23",
            "temp_change": 5.0
        }
        self.assertEqual(format_json(expected), self.wr.max_temp_delta())

    def test_simple_days_of_precip(self):
        args = {
            "function_name": "days-of-precip",
            "city": "jun",
            "month": None,
            "year": None
        }
        self.wr.set_args(MockArgs(args))
        expected = {
            "city": "jun",
            "days_of_precip": 1.3
        }
        self.assertEqual(format_json(expected), self.wr.days_of_precip())

    def test_days_of_precip_with_dates(self):
        args = {
            "function_name": "days-of-precip",
            "city": "jun",
            "month": 11,
            "year": 2017
        }
        self.wr.set_args(MockArgs(args))
        expected = {
            "city": "jun",
            "days_of_precip": 1.3
        }
        self.assertEqual(format_json(expected), self.wr.days_of_precip())

    def test_mia_location(self):
        args = {
            "function_name": "max-temp-delta",
            "city": "mia",
            "month": None,
            "year": None
        }
        self.wr.set_args(MockArgs(args))
        expected = {
            "city": "mia",
            "date": "2019-12-30",
            "temp_change": 15.0
        }
        self.assertEqual(format_json(expected), self.wr.max_temp_delta())


class MockArgs:
    def __init__(self, args):
        self.function_name = args['function_name']
        self.city = args['city']
        self.month = args['month']
        self.year = args['year']


if __name__ == "__main__":
    unittest.main()
