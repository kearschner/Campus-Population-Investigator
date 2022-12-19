from typing import Callable, Iterable, TypeVar, Dict
import CampusPop.SectionHandle as SectionHandle
import datetime
import functools

T = TypeVar("T");
U = TypeVar("U");
def recursiveReduce(composer : Callable[[T, T], T], baseCase : T) -> Callable[[U, Iterable[Callable[[U], T]]], T]:
	
	def generated(sharedInput : U, funcs : Iterable[Callable[[U], T]]) -> T:

		def underlyingComposition(value : T, func : Callable[[U], T]) -> T:
			return composer(value, func(sharedInput));

		return functools.reduce(underlyingComposition, funcs, baseCase);

	return generated;

		
def intersection(funcs : Iterable[Callable[[T], bool]]) -> Callable[[T], bool]:

	def underlyingIntersect(x : bool, y : bool) -> bool:
		return x and y;
		
	def generated(sharedInput : T) -> bool:
		return (recursiveReduce(underlyingIntersect, True))(sharedInput, funcs);

	return generated;


def union(funcs : Iterable[Callable[[T], bool]]) -> Callable[[T], bool]:

	def underlyingUnion(x : bool, y : bool) -> bool:
		return x and y;
		
	def generated(sharedInput : T) -> bool:
		return (recursiveReduce(underlyingUnion, False))(sharedInput, funcs);

	return generated;


T = TypeVar("T");
def filterIterable(lst : Iterable[T], filter : Callable[[T], bool]) -> Iterable[T]:
	return (elem for elem in lst if filter(elem));


def genDayFilter(day : SectionHandle.Day) -> Callable[[SectionHandle.Section], bool]:

	def generated(sec : SectionHandle.Section) -> bool:
		return day in sec.days;

	return generated;


def genTimeFilter(time : datetime.time) -> Callable[[SectionHandle.Section], bool]:
	
	def generated(sec : SectionHandle.Section) -> bool:
		return sec.timeFrame is not None and time in sec.timeFrame;

	return generated;


def accumulatePopulation(pop : int, sec : SectionHandle.Section) -> int:
	return pop + sec.filled;


def countPopOfSections(sections : Iterable[SectionHandle.Section]) -> int:
	return functools.reduce(accumulatePopulation, sections, 0);


S = TypeVar("S");
def reduceDict( function : Callable[[T, S], T],
				iterable : Iterable[S],
				default  : T,
				key      : Callable[[S], U]) -> Dict[U, T]:

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


def timeIter(startTime : datetime.time, endTime : datetime.time, minuteIncrement : int) -> Iterable[datetime.time]:

	currHour = startTime.hour;
	currMinute = startTime.minute;

	currTime = datetime.time(currHour, currMinute);
	while currTime < endTime:
		yield currTime;
		currMinute += minuteIncrement;
		if currMinute >= 60:
			currMinute -= 60;
			currHour += 1;
		
		if currHour >= 24:
			break;

		currTime = datetime.time(currHour, currMinute);


def popAcrossDay(sections : Iterable[SectionHandle.Section], day : SectionHandle.Day, minuteIncrement : int) -> Iterable[int]:

	dayFilter = genDayFilter(day)

	for t in timeIter(datetime.time.min, datetime.time.max, minuteIncrement):
		filtered = filterIterable(sections, intersection([dayFilter ,genTimeFilter(t)]));
		yield countPopOfSections(filtered);