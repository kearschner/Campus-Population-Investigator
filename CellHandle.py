import datetime
import enum
import functools
import typing

class Location():

    def __init__(self, locStr : str) -> None:
        self.building, self.room = locStr.split(' ');

    def __str__(self) -> str:
        return "%s %s" % (self.building, self.room);


class Day(enum.Flag):
    MON = enum.auto();
    TUE = enum.auto();
    WED = enum.auto();
    THU = enum.auto();
    FRI = enum.auto();
    SAT = enum.auto();
    SUN = enum.auto();

    @staticmethod
    def fromString(dayString : str) -> "Day":
        if dayString == "M":
            return Day.MON;
        if dayString == "T":
            return Day.TUE;
        if dayString == "W":
            return Day.WED;
        if dayString == "R":
            return Day.THU;
        if dayString == "F":
            return Day.FRI;
        if dayString == "S":
            return Day.SAT;
        if dayString == "U":
            return Day.SUN;

        return Day(0);


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
