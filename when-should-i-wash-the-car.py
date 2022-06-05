#!/usr/bin/env python3

"""Test Program."""
from __future__ import annotations

import asyncio
import logging
import time
import argparse

from statistics import median

from pyweatherbitdata.api import WeatherBitApiClient
from pyweatherbitdata.data import (
    ObservationDescription,
    BaseDataDescription,
    ForecastDescription
)
from pyweatherbitdata.exceptions import (
    InvalidApiKey,
    RequestError,
    ResultError,
)

_LOGGER = logging.getLogger(__name__)

def average(lst):
    return sum(lst) / len(lst)

def list_less(lst,less):
    for x in lst:
        if(x>less):
            return 0
    return 1

def wash(pop_list,threshold,duration):
    result = []
    p_list = []
    p_result = []
    for x in range(len(pop_list)):
        p_list.append(pop_list[x])
        if(len(p_list)>=duration):
            if(len(p_result)==5):
                if(p_result[3]>average(p_list)):
                    p_result = [duration, threshold, x-1, average(p_list), max(p_list)]
            else:
                p_result = [duration, threshold, x-1, average(p_list), max(p_list)]
            if(list_less(p_list,threshold)):
                result.append([duration, x-1, p_list.copy(), average(p_list), max(p_list)])
            p_list.pop(0)
    result.insert(0,p_result)
    return result

def print_wash(wash_list):
    if len(wash_list)>1:
        str="Based on {} day(s) period, best time to wash your car is in {} day(s) " \
            "with avearage of {:.2f}% chance (maximum {}% pop) of rain during this period."
        print(str.format(
                wash_list[1][0],
                wash_list[1][1],
                wash_list[1][3],
                wash_list[1][4]
                ))
    elif len(wash_list)==1:
        str="Unfortunately based on {} day(s) period, no good time to wash your car (with less then {:.2f}% pop), " \
            "best time to wash is in {} day(s) when average chance of rain will be {:.2f}% but with maximum change of {}."
        print(str.format(
                wash_list[0][0],
                wash_list[0][1],
                wash_list[0][2],
                wash_list[0][3],
                wash_list[0][4]
                ))
    else:
        print("Something wrong")

async def main() -> None:
    start = time.time()

    duration=3
    good_pop=60

    #TODO: move it to parameters
    weatherbit = WeatherBitApiClient(
        "12c4f93fc60a4161b0685bad13519735",
        49.223004, -122.774502,
        language="en",
    )

    try:
        await weatherbit.initialize()

    except InvalidApiKey as err:
        _LOGGER.debug(err)
    except RequestError as err:
        _LOGGER.debug(err)
    except ResultError as err:
        _LOGGER.debug(err)

#    data: BaseDataDescription = weatherbit.station_data
#    if data is not None:
#        for field in data.__dataclass_fields__:
#            value = getattr(data, field)
#            print(field, "-", value)
#
#    data: ObservationDescription = await weatherbit.update_sensors()
#    if data is not None:
#        for field in data.__dataclass_fields__:
#            value = getattr(data, field)
#            print(field, "-", value)

    data: ForecastDescription = await weatherbit.update_forecast()
    if data is not None:
        #print(data.forecast)
        
        pop = []
        for x in range(len(data.forecast)):
            pop.append(data.forecast[x].pop)

        print_wash(wash(pop,50,3))
        print_wash(wash(pop,60,7))

        _LOGGER.debug("POP schedule %s", pop)

    end = time.time()

    await weatherbit.req.close()

    _LOGGER.debug("Execution time: %s seconds", end - start)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Should you wash a car today?')
    parser.add_argument('-a','--address', help='Provide your location, like full address, or city with region', required=True)
    parser.add_argument('-d','--days', help='How many days you want to keep your car clean? (Default 3 days)', default='3')
    parser.add_argument('-p','--percentage', help="What average probability of precipitation you want to use? (Default 50%%)", default='50')
    parser.add_argument('--key',help="WeatherBitApiClient key if you have it", default='12c4f93fc60a4161b0685bad13519735"')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    #TODO: add arguments to the function
    #TODO: rename function to something unique
    asyncio.run(main())
