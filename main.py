import CampusPop.SectionHandle as SectionHandle
import CampusPop.TableParser as TableParser
import CampusPop.Analysis as Analysis
import datetime
import matplotlib.pyplot as plt
import operator

allSections : list[SectionHandle.Section] = list(TableParser.sectionsFromTableDump("oasisDump.txt"));

choices = list(Analysis.initMultipleCourses(["CNT 4419", "COP 4710", "COT 4210", "CAP 4401", "MAD 4301"]))

def priorityFunc(course : SectionHandle.Course) -> SectionHandle.RegistrationPriority:
	for req in choices[:3]:
		if course == req:
			return SectionHandle.RegistrationPriority.NEEDED;
	return SectionHandle.RegistrationPriority.FILLER;

possibilities = Analysis.getPossibleSchedules(allSections, choices, priorityFunc);

for i, possib in enumerate(possibilities):
	print("Possibility %d:\n" % i);
	for secGroup in possib:
		for sec in secGroup:
			print(sec.scheduleInformation);
		print("\n");
	print("\n\n");


'''
allBuildings = Analysis.setOfKeys(allSections, lambda sec: sec.getBuilding());
print(allBuildings);


sorted([datetime.datetime(1,1,1), datetime.datetime(2,2,2)])

buildingInfo = Analysis.mapRoomsToSections("che", Analysis.filterIterable(allSections, Analysis.genDayFilter(SectionHandle.Day.MON)));

#print([len(secs) for secs in cheInfo.values()])

#cheInfo = Analysis.operateOnDict(lambda secGroup : [sec.location for sec in secGroup], cheInfo);

#print([str(sec) for sec in cheInfo["103"]]);

roomEstCapacity = Analysis.operateOnDict(Analysis.getHighestCapacity, buildingInfo);

for room, cap in roomEstCapacity.items():
	print(room, "->", cap);

roomUsages = Analysis.operateOnDict(Analysis.getTimespans, buildingInfo);

roomUsages = Analysis.operateOnDict(Analysis.compose(Analysis.timespanMultiUnion, Analysis.getTimespans), buildingInfo);

for room, usage in roomUsages.items():
	print(room, "->", end='');
	print([span for span in usage]);


#filtered = Analysis.filterIterable(allSections, Analysis.intersection( [Analysis.genBuildingFilter("CMC"), Analysis.genInstructionMethodFilter(SectionHandle.InstructionalMethod.CLASSROOM)]));
#print([cmcSec for cmcSec in filtered])
'''
