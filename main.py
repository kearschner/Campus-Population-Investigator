import CampusPop.SectionHandle as SectionHandle
import CampusPop.TableParser as TableParser
import CampusPop.Analysis as Analysis
import datetime
import matplotlib.pyplot as plt
import operator

allSections : list[SectionHandle.Section] = list(TableParser.sectionsFromTableDump("oasisDump.txt"));

'''
allBuildings = Analysis.setOfKeys(allSections, lambda sec: sec.getBuilding());
print(allBuildings);
'''

buildingInfo = Analysis.mapRoomsToSections("che", Analysis.filterIterable(allSections, Analysis.genDayFilter(SectionHandle.Day.MON)));

#print([len(secs) for secs in cheInfo.values()])

#cheInfo = Analysis.operateOnDict(lambda secGroup : [sec.location for sec in secGroup], cheInfo);

#print([str(sec) for sec in cheInfo["103"]]);

roomEstCapacity = Analysis.operateOnDict(Analysis.getHighestCapacity, buildingInfo);

for room, cap in roomEstCapacity.items():
	print(room, "->", cap);

roomUsages = Analysis.operateOnDict(Analysis.getTimespans, buildingInfo);

roomUsages = Analysis.operateOnDict(Analysis.composeFunctions(Analysis.timespanMultiUnion, Analysis.getTimespans), buildingInfo);

for room, usage in roomUsages.items():
	print(room, "->", end='');
	print([span.strWithFormatter(SectionHandle.justTimeStr) for span in usage]);


#filtered = Analysis.filterIterable(allSections, Analysis.intersection( [Analysis.genBuildingFilter("CMC"), Analysis.genInstructionMethodFilter(SectionHandle.InstructionalMethod.CLASSROOM)]));
#print([cmcSec for cmcSec in filtered])
