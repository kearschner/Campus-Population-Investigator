import datetime
import functools
import typing

import CampusPop.SectionHandle as SectionHandle




@functools.cache
def convertDays(daysString : str) -> SectionHandle.Day:
    days = SectionHandle.Day(0);

    for day in daysString:
        days |= SectionHandle.Day.fromString(day);

    return days;

@functools.lru_cache(maxsize=24)
def hourMap(num : int, afternoon : bool) -> int:
    if not afternoon:
        return num % 12;
    
    if num == 12:
        return 12;
    
    return num + 12;

def convertTime(timeString : str) -> typing.Optional[datetime.time]:

    if "N/A" in timeString:
        return None;

    if "TBA" in timeString:
        return None;

    afternoon : bool = 'pm' in timeString;
    
    hour = hourMap(int(timeString[:2]), afternoon);
    
    return datetime.time(hour, int(timeString[3:5]));


def convertDate(timeString : str) -> datetime.date:

    return datetime.date(2001, int(timeString[:2]), int(timeString[-2:]));


T = typing.TypeVar('T')
def convertRange(operation : typing.Callable[[str], typing.Optional[SectionHandle.SelfComparable]], sep : str) -> typing.Callable[[str], typing.Optional[SectionHandle.Range]]:

    def conversionFunc(input : str) -> typing.Optional[SectionHandle.Range]:
        if sep not in input:
            return None;
        endPoints : list[str] = input.split(sep);
        start = operation(endPoints[0]);
        end = operation(endPoints[1]);

        if start is None or end is None:
            return None;
        return SectionHandle.Range(start, end);

    return conversionFunc;


convertTimeFrame = functools.cache(convertRange(convertTime, '-'));

convertTermDates = functools.cache(convertRange(convertDate, '-'));


def convertLocation(locString : str) -> typing.Optional[SectionHandle.Location]:

    if "TBA" in locString:
        return None;

    return SectionHandle.Location(locString);

def convertSeats(capString : str, availString : str) -> int:
    return int(capString) - int(availString);

def isPermitLocked(permString : str) -> bool:
    return 'Y' == permString; 