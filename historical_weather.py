#!/usr/bin/env python
import argparse
import json
import sys
import pandas as pd

cli_error_str = 'historical_weather.py: error:'
CSV_FILE = 'data/noaa_historical_weather_10yr.csv'


class WeatherReport:

    valid_cities = {
        "bos": "USW00014739",
        "jun": "USW00025309",
        "mia": "USW00012839"
    }

    def __init__(self, csvfile):
        self.filename = csvfile
        self.valid_funcs = {
            'days-of-precip': self.days_of_precip,
            'max-temp-delta': self.max_temp_delta
        }
        self.function = None
        self.city = None
        self.year = None
        self.month = None

    def valid_input(self, parser):
        args = parser.parse_args()
        if args.function_name not in self.valid_funcs.keys():
            parser.print_usage()
            print(f'{cli_error_str} Function name must be one of: days-of-precip or max-temp-delta')
            exit(1)
        if args.city not in WeatherReport.valid_cities.keys():
            parser.print_usage()
            print(f'{cli_error_str} City name must be one of: bos, jun, mia')
            exit(1)
        if args.function_name == 'max-temp-delta':
            if args.month and not args.year:
                parser.print_usage()
                print(f'{cli_error_str} You must specify a year if you specify a month.')
                exit(1)
            if args.month and args.month not in range(1, 13):
                parser.print_usage()
                print(f'{cli_error_str} Month must be between 1 and 12.')
                exit(1)
            if args.year and args.year not in range(2010, 2020):
                parser.print_usage()
                print(f'{cli_error_str} Year must be between 2010 and 2019.')
                exit(1)
        self.set_args(args)
        return True

    def set_args(self, args):
        self.function = args.function_name
        self.city = args.city
        self.year = args.year
        self.month = args.month

    def run(self):
        print(self.valid_funcs[self.function]())

    def days_of_precip(self):
        """Return avg yearly days of precipitation for a particular city (including snowfall)

        Example output:
        {
            "city": "bos",
            "days_of_precip": 34.5
        }
        """
        df = pd.read_csv(self.filename, usecols=['STATION', 'DATE', 'PRCP', 'SNOW'])
        city_station = WeatherReport.valid_cities[self.city]
        city_df = df[df['STATION'].str.match(city_station)].copy()
        total_prcp = city_df['PRCP'] + city_df['SNOW']
        city_df['TOTAL_PRCP'] = total_prcp
        groupby_year_df = city_df.groupby([pd.to_datetime(df['DATE'], format='%Y-%m-%d').dt.year])
        avg_yearly_days_of_prcp = groupby_year_df.apply(lambda x: (x['TOTAL_PRCP'] > 0).sum()).mean()
        result = {
            "city": self.city,
            "days_of_precip": avg_yearly_days_of_prcp
        }
        return json.dumps(result, indent=4)

    def max_temp_delta(self):
        """Return greatest daily temp change for a particular city

        Example output:
        {
            "city": "bos",
            "date": "2012-12-31",
            "temp_change": 5.3
        }
        """
        df = pd.read_csv(self.filename, usecols=['STATION', 'DATE', 'TMAX', 'TMIN'])
        city_station = WeatherReport.valid_cities[self.city]
        city_df = df[df['STATION'].str.match(city_station)].copy()
        if self.month or self.year:
            city_df = self._filter_df_with_timerange(city_df)
        temp_delta = city_df['TMAX'] - city_df['TMIN']
        city_df['TEMP_DELTA'] = temp_delta
        max_row = city_df[city_df['TEMP_DELTA'] == city_df['TEMP_DELTA'].max()]
        result = {
            "city": self.city,
            "date": max_row['DATE'].values[0],
            "temp_change": max_row['TEMP_DELTA'].values[0]
        }
        return json.dumps(result, indent=4)

    def _filter_df_with_timerange(self, df):
        df_by_year = df[pd.to_datetime(df['DATE'], format='%Y-%m-%d').dt.year == self.year].copy()
        if self.month:
            df_by_year_and_month = df_by_year[pd.to_datetime(df_by_year['DATE'], format='%Y-%m-%d').dt.month == self.month].copy()
            return df_by_year_and_month
        else:
            return df_by_year


if __name__ == '__main__':
    help_description = """
Get historical weather data b/w 2010-2019.
* days-of-precip: avg yearly days of precipitation for a particular city (including snowfall)
* max-temp-delta: greatest daily temperature change for a particular city (in C)"""
    parser = argparse.ArgumentParser(description=help_description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('function_name', type=str, help='must be one of: days-of-precip or max-temp-delta')
    parser.add_argument('city', type=str, help='must be one of: bos, jnu, or mia')
    parser.add_argument('--year', type=int, help='restrict search to a particular year b/w 2010-2019 (required if month specified)')
    parser.add_argument('--month', type=int, help='restrict search to a particular month (i.e., 1-12)')

    if any(option in sys.argv for option in ['-h', '--help']):
        parser.print_help()
        exit(0)
    if len(sys.argv) < 3:
        parser.print_usage()
        print(f'{cli_error_str} the following arguments are required: function_name, city')
        sys.exit(1)

    wr = WeatherReport(CSV_FILE)
    if wr.valid_input(parser):
        wr.run()
