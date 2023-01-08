import CampusPop.SectionHandle as SectionHandle
import CampusPop.TableParser as TableParser
import CampusPop.Analysis as Analysis

from collections.abc import Iterable, Callable


def parseRequest(requestLine : str) -> tuple[SectionHandle.Course, SectionHandle.RegistrationPriority]:

    subject, courseNumber, priorityFlag = requestLine.split(' '); 
    
    course = SectionHandle.Course(subject, courseNumber);

    if priorityFlag == '1':
        return course, SectionHandle.RegistrationPriority.NEEDED;
    
    return course, SectionHandle.RegistrationPriority.FILLER;


def parseRequests(secRequests : Iterable[str]) -> tuple[Iterable[SectionHandle.Course], Callable[[SectionHandle.Course], SectionHandle.RegistrationPriority]]:

    courseRegPriorityPairs = [parseRequest(reqLine) for reqLine in secRequests];

    priorityFunc = Analysis.dictAsCallable(dict(courseRegPriorityPairs));

    return (coursePriorityPair[0] for coursePriorityPair in courseRegPriorityPairs), priorityFunc;

secRequestsFile = open("classes.txt", "r");

choices, priorityFunc = parseRequests(secRequestsFile.readlines());

allSections : list[SectionHandle.Section] = list(TableParser.sectionsFromTableDump("oasisDump.txt"));

possibilities = Analysis.getPossibleSchedules(allSections, list(choices), priorityFunc);

for i, possib in enumerate(possibilities):
	print("Possibility %d:\n" % i);
	for secGroup in possib:
		for sec in secGroup:
			print(sec.scheduleInformation);
		print("\n");
	print("\n\n");
