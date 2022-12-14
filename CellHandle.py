import datetime
import functools
import typing

from SectionHandle import Day, Location, Section





def convertDays(daysString : str) -> Day:
    days = Day(0);

    for day in daysString:
        days |= Day.fromString(day);

    return days;


def convertTime(timeString : str) -> datetime.time:

    afternoon : bool = 'pm' in timeString;
    
    hour = int(timeString[:2]);
    hour = hour + 12 if afternoon else hour;
    
    return datetime.time(hour, int(timeString[2:4]));


def convertDate(timeString : str) -> datetime.date:

    return datetime.date(2001, int(timeString[:2]), int(timeString[-2:]));


T = typing.TypeVar('T')
def convertEach(operation : typing.Callable[[str], T], sep : str) -> typing.Callable[[str], tuple[T]]:

    return lambda input : tuple(map(operation, input.split(sep)));


convertTimeFrame = functools.cache(convertEach(convertTime, '-'));

convertTermDates = functools.cache(convertEach(convertDate, '-'));


def convertLocation(locString : str) -> typing.Optional[Location]:

    if "TBA" in locString:
        return None;

    return Location(locString);

def convertSeats(capString : str, availString : str) -> int:
    return int(capString) - int(availString);