
# Historical Weather CLI

```
usage: historical_weather.py [-h] [--year YEAR] [--month MONTH] function_name city

Get historical weather data b/w 2010-2019.
* days-of-precip: avg yearly days of precipitation for a particular city (including snowfall)
* max-temp-delta: greatest daily temperature change for a particular city (in C)

positional arguments:
  function_name  must be one of: days-of-precip or max-temp-delta
  city           must be one of: bos, jnu, or mia

optional arguments:
  -h, --help     show this help message and exit
  --year YEAR    restrict search to a particular year b/w 2010-2019 (required if month specified)
  --month MONTH  restrict search to a particular month (i.e., 1-12)

```

Data from the [Climate Data Online](https://www.ncdc.noaa.gov/cdo-web/search) tool provided by NOAA.


## Assumptions

* Though what we think of as 'precipitation' usually includes snowfall, somewhat confusingly, the PRCP column of the NOAA data looks like it does not include SNOW (e.g., line 12 - PRCP: 2.3, SNOW: 43.0). So in calculating the days of precipitation, I have considered a nonzero value in either of these columns as counting towards a day of precipitation.

