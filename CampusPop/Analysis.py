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
		for lecture in sec.lectureDays:
			if lecture.timeFrame is None:
				continue;
			if day in lecture.days and time in lecture.timeFrame:
				return True;
		return False;

	return genedFilter;


def accumulatePopulation(pop : int, sec : SectionHandle.Section) -> int:
	return pop + sec.filled;

def countPopOfSections(sections : typing.Iterable[SectionHandle.Section]) -> int:
	return functools.reduce(accumulatePopulation, sections, 0);

S = typing.TypeVar("S");

U = typing.TypeVar("U", contravariant=True, bound="Stringable");
class Stringable(typing.Protocol):
    def __str__(self) -> str:
        ...

def reduceDict(function : typing.Callable[[T, S], T],
               iterable : typing.Iterable[S],
               default  : T,
               key      : typing.Callable[[S], Stringable]):

    results = collections.defaultdict(default_factory=default);
    it = iter(iterable);

    for element in it:
        currKey = key(element);
        results[currKey] = function(results[currKey], element);
    
    pass
