import enum
from dataclasses import dataclass
import typing
import datetime

def justTimeStr(dt : datetime.datetime) -> str:
	return "%02d:%02d" % (dt.hour, dt.minute);

def datetimeOnArbDate(hour : int, minute : int) -> datetime.datetime:
	return datetime.datetime(9999, 1, 1, hour, minute);


@dataclass(frozen=True, eq=True)
class Course:
	subject : str;
	courseNumber : str;

	def __str__(self) -> str:
		return "%s %s" % (self.subject, self.courseNumber);


@dataclass(frozen=True, eq=True)
class Location:
	building : str;
	room : str;

	def __str__(self) -> str:
		return "%s %s" % (self.building, self.room);

	@staticmethod
	def fromFullString(locStr : str) -> "Location":
		return Location(*locStr.split(' '))



C = typing.TypeVar("C", contravariant=True, bound="SelfComparable");
class SelfComparable(typing.Protocol):
	def __le__(self : C, other : C, /) -> bool:
		...
	
	def __lt__(self : C, other : C, /) -> bool:
		...

	def __gt__(self : C, other : C, /) -> bool:
		...


class Range(typing.Generic[C]):

	def __init__(self, start : C, end : C):
		if end < start:
			raise ValueError("start must be less than or equal to end.");
		self.start : C = start;
		self.end : C = end;
	
	def __str__(self) -> str:
		return "%s-%s" % (self.start, self.end);

	def strWithFormatter(self, formatter : typing.Callable[[C], str]):
		return "%s-%s" % (formatter(self.start), formatter(self.end))

	def __repr__(self) -> str:
		return "Range(start=%s, end=%s)" % (repr(self.start), repr(self.end));

	def __contains__(self, value : C) -> bool:
		return self.start <= value and value <= self.end;

	def __eq__(self, other : "Range[C]") -> bool:
		return self.start == other.start and self.end == other.end;

	def __lt__(self, other : "Range[C]") -> bool:
		return self.start < other.start;

	def wraps(self, other : "Range[C]") -> bool:
		return self.start <= other.start and other.end <= self.end;
	
	@staticmethod
	def genEpsilonedUnion(epsilon : typing.Any) -> typing.Callable[["Range[C]", "Range[C]"], typing.Optional["Range[C]"]]:

		def union(a : Range[C], b : Range[C]) -> typing.Optional[Range[C]]:

			if a.wraps(b):
				return a;

			if b.wraps(a):
				return b;

			if a < b:
				low = a;
				high = b;
			else:
				low = b;
				high = a;

			if high.start <= low.end + epsilon :
				return Range(a.start, b.end);	

			return None;

		return union;

	@staticmethod
	def intersection(a : "Range[C]", b : "Range[C]") -> typing.Optional["Range[C]"]:

		if a.wraps(b):
			return b;

		if b.wraps(a):
			return a;

		if a < b:
			low = a;
			high = b;
		else:
			low = b;
			high = a;

		if high.start < low.end:
			return Range(high.start, low.end);

		return None;



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


class InstructionalMethod(enum.Flag):
	ALL_ONLINE = enum.auto();
	CLASSROOM = enum.auto();
	FLEXIBLE = enum.auto();
	HYBRID = enum.auto();
	DISTANCE_LEARNING = enum.auto();
	NOT_APPLICABLE = enum.auto();

	@staticmethod
	def fromString(methodString : str) -> "InstructionalMethod":
		if methodString == "All Online":
			return InstructionalMethod.ALL_ONLINE;
		if methodString == "Classroom":
			return InstructionalMethod.CLASSROOM;
		if methodString == "Flexible Online/In-Person":
			return InstructionalMethod.FLEXIBLE;
		if methodString == "Hybrid Blend":
			return InstructionalMethod.HYBRID;
		if methodString == "Primarily DL":
			return InstructionalMethod.DISTANCE_LEARNING;

		return InstructionalMethod.NOT_APPLICABLE;


@dataclass(frozen=True)
class Section:
	crn : str;
	course : Course;
	sectionNumber : str;
	credits : str;
	name : str;
	method : InstructionalMethod;
	permit : bool;
	termDates : typing.Optional[Range[datetime.datetime]];
	days : Day;
	timeFrame : Range;
	capacity : int;
	availability : int;
	instructors : str;
	campus : str;
	location : typing.Optional[Location];
	attributes : str;

	filled = property(lambda self: self.capacity - self.availability, None, None, "Number of seats currently filled in the section.");

	def __str__(self) -> str:
		return "CRN: %s, Sec: %s, Cred: %s\nCourse: %s - %s\nMethod: %s, Permit: %s\nTerm:%s, Day: %s, Time: %s, Loc: %s\nCap: %d, Avail: %d\nInstructors: %s, Campus:%s, Attributes:%s" % (self.crn, self.sectionNumber, self.credits, self.name, self.course, self.method, self.permit, self.termDates, self.days, self.timeFrame.strWithFormatter(justTimeStr), self.location, self.capacity, self.availability, self.instructors, self.campus, self.attributes);

	def copyForNewDay(self, termDates : typing.Optional[Range], days : Day, timeFrame : Range, instructors : str, campus: str, location :  typing.Optional[Location], attributes : str) -> typing.Self:
		return Section(self.crn, self.course, self.sectionNumber, self.credits, self.name, self.method, self.permit, termDates, days, timeFrame, self.capacity, self.availability, instructors, campus, location, attributes);

	def getBuilding(self) -> str:
		loc = self.location;
		if loc is None:
			return "TBA";
		return loc.building;

	def getRoom(self) -> str:
		loc = self.location;
		if loc is None:
			return "TBA";
		return loc.room;

	def getCourse(self) -> Course:
		return self.course;

	def getCRN(self) -> str:
		return self.crn;


