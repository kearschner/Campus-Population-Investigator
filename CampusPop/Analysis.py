import typing
import CampusPop.SectionHandle as SectionHandle
import datetime
import functools
import collections

T = typing.TypeVar("T");
def filterIterable(lst : typing.Iterable[T], filter : typing.Callable[[T], bool]) -> typing.Iterable[T]:
	return (elem for elem in lst if filter(elem));

def genFilterAtDayAndTime(day : SectionHandle.Day, time : datetime.time) -> typing.Callable[[SectionHandle.Section], bool]:

	def genedFilter(sec : SectionHandle.Section) -> bool:
		return (sec.timeFrame is not None) and (day in sec.days and time in sec.timeFrame);

	return genedFilter;


def accumulatePopulation(pop : int, sec : SectionHandle.Section) -> int:
	return pop + sec.filled;

def countPopOfSections(sections : typing.Iterable[SectionHandle.Section]) -> int:
	return functools.reduce(accumulatePopulation, sections, 0);

S = typing.TypeVar("S");
def reduceDict( function : typing.Callable[[T, S], T],
				iterable : typing.Iterable[S],
				default  : T,
				key      : typing.Callable[[S], str])-> typing.Dict[str, T]:

	results = dict()
	it = iter(iterable);

	for element in it:
		currKey = key(element);
		results[currKey] = function(results.get(currKey,default), element);
		
	return results;


def getBuilding(section : SectionHandle.Section) -> str:
	loc = section.location;
	if loc is None:
		return "TBA";
	return loc.building;
