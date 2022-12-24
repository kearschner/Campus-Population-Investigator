from typing import TypeVar, Optional 
from collections.abc import Callable, Iterable, Container, Iterator
import CampusPop.SectionHandle as SectionHandle
import datetime
import functools
import itertools

T = TypeVar("T");
U = TypeVar("U");
S = TypeVar("S");

def compose(f : Callable[[T], S], g : Callable[[U], T]) -> Callable[[U], S]:

	return lambda x : f(g(x));



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
def filterIterable(lst : Iterable[T], filter : Callable[[T], bool]) -> Iterator[T]:
	return (elem for elem in lst if filter(elem));


def genDayFilter(day : SectionHandle.Day) -> Callable[[SectionHandle.Section], bool]:

	def generated(sec : SectionHandle.Section) -> bool:
		return day in sec.days;

	return generated;


def genTimeFilter(time : datetime.datetime) -> Callable[[SectionHandle.Section], bool]:
	
	def generated(sec : SectionHandle.Section) -> bool:
		return sec.timeFrame is not None and time in sec.timeFrame;

	return generated;


def genBuildingFilter(building : str) -> Callable[[SectionHandle.Section], bool]:

	def generated(sec : SectionHandle.Section) -> bool:
		return SectionHandle.Section.getBuilding(sec).upper() == building.upper();

	return generated;


def genInstructionMethodFilter(method : SectionHandle.InstructionalMethod) -> Callable[[SectionHandle.Section], bool]:

	def generated(sec : SectionHandle.Section) -> bool:
		return sec.method in method;

	return generated;


def genCoursesFilter(courses : Container[SectionHandle.Course]) -> Callable[[SectionHandle.Section], bool]:

	def generated(sec : SectionHandle.Section) -> bool:
		return sec.getCourse() in courses;

	return generated;


def accumulatePopulation(pop : int, sec : SectionHandle.Section) -> int:
	return pop + sec.filled;


def countPopOfSections(sections : Iterable[SectionHandle.Section]) -> int:
	return functools.reduce(accumulatePopulation, sections, 0);


S = TypeVar("S");
def reduceDict( function : Callable[[T, S], T],
				iterable : Iterable[S],
				default  : T,
				key      : Callable[[S], U]) -> dict[U, T]:

	results = dict()
	it = iter(iterable);

	for element in it:
		currKey = key(element);
		results[currKey] = function(results.get(currKey,default), element);
		
	return results;


def trimWhile( pred : Callable[[T], bool], iterable : Iterable[T]) -> Iterable[T]:

	it = iter(iterable);
	
	itertools.dropwhile(pred, it);
	it = reversed(list(it));

	itertools.dropwhile(pred, it);
	return reversed(list(it));


def timeIter(startTime : datetime.datetime, endTime : datetime.datetime, increment : datetime.timedelta) -> Iterable[datetime.datetime]:

	currTime = startTime;

	while currTime < endTime:
		yield currTime;
		currTime += increment;


def popAcrossDay(sections : Iterable[SectionHandle.Section], day : SectionHandle.Day, increment : datetime.timedelta) -> Iterable[int]:

	dayFilter = genDayFilter(day)

	for t in timeIter(SectionHandle.datetimeOnArbDate(0,0), SectionHandle.datetimeOnArbDate(23,59), increment):
		filtered = filterIterable(sections, intersection([dayFilter ,genTimeFilter(t)]));
		yield countPopOfSections(filtered);


# All types of inefficent :(
def bucketBy(iterable : Iterable[T], key : Callable[[T], U]) -> dict[U, list[T]]:

	it = iter(iterable);
	results = dict();

	for elem in it:
		currKey = key(elem);
		inBucket = results.get(currKey, []);
		if not inBucket:
			results[currKey] = inBucket;
		inBucket.append(elem);

	return results;


def operateOnDict(function : Callable[[S], U], dictionary : dict[T, S]) -> dict[T, U]:

	outDict = dict();

	for key, val in dictionary.items():
		outDict[key] = function(val);

	return outDict;


def sortedByTimespan(sections : Iterable[SectionHandle.Section]) -> list[SectionHandle.Section]:
	return sorted(sections, key=lambda sec : sec.timeFrame)


def getTimespans(sections : Iterable[SectionHandle.Section]) -> Iterable[SectionHandle.Range]:
	for sec in sections:
		yield sec.timeFrame;


def mapRoomsToSections(inBuilding : str, sections : Iterable[SectionHandle.Section]) -> dict[str, list[SectionHandle.Section]]:
	return operateOnDict(sortedByTimespan, bucketBy(filterIterable(sections, genBuildingFilter(inBuilding)), SectionHandle.Section.getRoom))


def genMultiUnion(unionFunc : Callable[[T, T], Optional[T]]) -> Callable[[Iterable[T]], Iterable[T]]:

	def unionMany(iterable : Iterable[T]) -> Iterable[T]:

		it = iter(iterable);
		saved : list[T] = [];

		top = next(it, None);

		if top is None:
			return;

		for elem in it:

			unionCandidate = unionFunc(top, elem);

			if unionCandidate is None:
				saved.append(elem);
				continue;

			top = unionCandidate;

		yield top;

		for recurUnion in unionMany(saved):
			yield recurUnion;

	return unionMany;

timespanMultiUnion = genMultiUnion(SectionHandle.Range.genEpsilonedUnion(datetime.timedelta(minutes=15)))


def setOfKeys(iterable : Iterable[T], key : Callable[[T], S]) -> set[S]:
	return {key(elem) for elem in iterable};

RichCompS = TypeVar("RichCompS", bound=SectionHandle.SelfComparable);
def reduceMax(subFunction : Callable[[T], RichCompS], iterable : Iterable[T], initial : RichCompS) -> RichCompS:
	def reductionFunc(value, element):
		return max(value, subFunction(element));
	
	return functools.reduce(reductionFunc, iterable, initial);

def getHighestCapacity(sections : Iterable[SectionHandle.Section]) -> int:
	
	def getCapacity(sec : SectionHandle.Section) -> int:
		return sec.capacity;

	return reduceMax(getCapacity, sections, 0);


def hasSectionOverlap(secA : SectionHandle.Section, secB : SectionHandle.Section) -> bool:

	if not secA.days & secB.days:
		return False;

	return SectionHandle.Range.intersection(secA.timeFrame, secB.timeFrame) is not None;


def hasScheduleOverlap(targetCRNGroup : Iterable[SectionHandle.Section], schedule : Iterable[Iterable[SectionHandle.Section]]) -> bool:

	underlyingScheduleSections = list(itertools.chain.from_iterable(schedule));

	for secPair in itertools.product(targetCRNGroup, underlyingScheduleSections):
		if hasSectionOverlap(secPair[0], secPair[1]):
			return True;
	
	return False;


def sectionsIntoCourseGroups(sections : Iterable[SectionHandle.Section]) -> Iterable[tuple[SectionHandle.Course, tuple[tuple[SectionHandle.Section]]]]:
	for sharedCourse, courseGroup in itertools.groupby(sections, SectionHandle.Section.getCourse):
		yield sharedCourse, tuple((tuple(crnGroupPair[1]) for crnGroupPair in itertools.groupby(courseGroup, SectionHandle.Section.getCRN)));


def optimizeSchedule(required : list[tuple[SectionHandle.Course, tuple[tuple[SectionHandle.Section]]]],
					 optional : list[tuple[SectionHandle.Course, tuple[tuple[SectionHandle.Section]]]]) -> Iterable[set[tuple[SectionHandle.Section]]]:

	requiredSize = len(required);
	optionalSize = len(optional);

	def buildOptionalSchedule(schedule : set[tuple[SectionHandle.Section]], groupIndex : int) -> Iterable[set[tuple[SectionHandle.Section]]]:

		hasSuccessPath = False;

		for targetCRNGroup in optional[groupIndex][1]:
			
			if hasScheduleOverlap(targetCRNGroup, schedule):
				continue;

			newSchedule = schedule | set([targetCRNGroup]);

			if groupIndex + 1 != optionalSize:
				yield from buildOptionalSchedule(newSchedule, groupIndex + 1);
				hasSuccessPath = True;
				continue;

			yield newSchedule;

		if not hasSuccessPath:
			yield schedule;


	def buildRequiredSchedule(schedule : set[tuple[SectionHandle.Section]], groupIndex : int) -> Iterable[set[tuple[SectionHandle.Section]]]:

		for targetCRNGroup in required[groupIndex][1]:
			
			if hasScheduleOverlap(targetCRNGroup, schedule):
				continue;

			newSchedule = schedule | set([targetCRNGroup]);

			if groupIndex + 1 != requiredSize:
				yield from buildRequiredSchedule(newSchedule, groupIndex + 1);
				continue;

			if optionalSize != 0:
				yield from buildOptionalSchedule(newSchedule, 0);
				continue;

			yield newSchedule;



	yield from buildRequiredSchedule(set(), 0);


def getPossibleSchedules( sections : Iterable[SectionHandle.Section], 
						  requestedClasses : Container[SectionHandle.Course],
						  priorityFunction : Callable[[SectionHandle.Course], SectionHandle.RegistrationPriority]) -> Iterable[Iterable[Iterable[SectionHandle.Section]]]:
	
	sections = filterIterable(sections, genCoursesFilter(requestedClasses));

	courseGroupsByPriority = bucketBy(sectionsIntoCourseGroups(sections), compose(priorityFunction, lambda courseGroupPair : courseGroupPair[0])) 

	print(courseGroupsByPriority);

	requiredClasses = courseGroupsByPriority[SectionHandle.RegistrationPriority.NEEDED];
	optionalClasses = courseGroupsByPriority[SectionHandle.RegistrationPriority.FILLER];
	
	return optimizeSchedule(requiredClasses, optionalClasses);


def initMultipleCourses(courseStrings : Iterable[str]) -> Iterable[SectionHandle.Course]:
	return map(SectionHandle.Course.fromFullString, courseStrings);