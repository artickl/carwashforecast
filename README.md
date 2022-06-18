# CarWashForecast
Should I was the car today? If not - then when?

# Requirements
Python Wrapper for WeatherBit API
- https://github.com/briis/py-weatherbit
```
pip install pyweatherbitdata
```

Free API key from https://www.weatherbit.io/
- More info in https://github.com/briis/py-weatherbit#readme

# How to use

```
$ ./when-should-i-wash-the-car.py -h
usage: when-should-i-wash-the-car.py [-h] -a ADDRESS [-d DAYS] [-p PERCENTAGE] [--key KEY]

Should you wash a car today?

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        Provide your location, like full address, or city with region (Coordinates are allowed too)
  -d DAYS, --days DAYS  How many days you want to keep your car clean? (Default 3 days)
  -p PERCENTAGE, --percentage PERCENTAGE
                        What average probability of precipitation you want to use? (Default 50%)
  --key KEY             WeatherBitApiClient key if you have it

$ cp .env.example .env
$ echo "KEY=######" > .env
$ . .env

$ ./when-should-i-wash-the-car.py -a "Maple Ridge" -d 7 -p 50 --key $KEY
Based on 7 day(s) period, best time to wash your car is in 5 day(s) with average of 19.29% chance (maximum 35% pop) of rain during this period.
```

# TODO
- need to think how to use it more efficiently (userfriendly)
- will be good to use city + country as an option, instead of coordinates
