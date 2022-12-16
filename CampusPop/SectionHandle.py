import datetime
import enum
from dataclasses import dataclass
import functools
import typing


@dataclass
class Course:
	subject : str;
	courseNumber : str;

	def __str__(self) -> str:
		return "%s %s" % (self.subject, self.courseNumber);

class Location:

    def __init__(self, locStr : str) -> None:
        self.building, self.room = locStr.split(' ');

    def __str__(self) -> str:
        return "%s %s" % (self.building, self.room);


C = typing.TypeVar("C", contravariant=True, bound="SelfComparable");
class SelfComparable(typing.Protocol):
	def __le__(self : C, other : C, /) -> bool:
		...
	
	def __ge__(self : C, other : C, /) -> bool:
		...

class Range():

	def __init__(self, start : SelfComparable, end : SelfComparable):
		self.start : SelfComparable = start;
		self.end : SelfComparable = end;
	
	def __str__(self) -> str:
		return "%s-%s" % (self.start, self.end);

	def __contains__(self, value : SelfComparable) -> bool:
		return value >= self.start and value <= self.end;

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

class InstructionalMethod(enum.Enum):
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

@dataclass
class LectureDay:
	termDates : typing.Optional[Range];
	days : Day;
	timeFrame : typing.Optional[Range];
	instructors : str;
	campus : str;
	location : typing.Optional[Location];
	attributes : str;

class Section:

	def __init__(self, 
				crn : str,
				course : Course,
				sec : str,
				credits : str,
				name : str,
				method : InstructionalMethod,
				permit : bool,
				capacity : int,
				availability : int) -> None:

		self.crn : str = crn;
		self.course : Course = course;
		self.sectionNumber : str = sec;
		self.credits : str = credits;
		self.name : str = name;
		self.method : InstructionalMethod = method;
		self.permit : bool = permit;
		self.capacity : int = capacity;
		self.availability : int = availability;

		self.lectureDays : list[LectureDay] = [];

	filled = property(lambda self: self.capacity - self.availability, None, None, "Number of seats currently filled in the section.");

	def getLectureByDay(self, day : Day) -> typing.Optional[LectureDay]:
		for lect in self.lectureDays:
			if day in lect.days:
				return lect;
		return None;
		
	def __str__(self) -> str:
		if not self.lectureDays:
			return "Section not fully initialized";

		out = "CRN: %s, Course: %s, Sect: %s, Creds: %s, Name: %s, Method: %s, Permit: %s, Cap: %s, Avail: %s\n" % (self.crn, self.course, self.sectionNumber, self.credits, self.name, self.method, self.permit, self.capacity, self.availability);
		for lect in self.lectureDays:
			out += "\tTerm: %s, Days: %s, Time: %s, Instructor: %s, Campus: %s, Loc: %s, Attrib: %s\n" % (lect.termDates, lect.days, lect.timeFrame, lect.instructors, lect.campus, lect.location, lect.attributes);

		return out;
		

