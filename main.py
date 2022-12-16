import CampusPop.SectionHandle as SectionHandle
import CampusPop.TableParser as TableParser
import CampusPop.Analysis as Analysis
import datetime

allSections : list[SectionHandle.Section] = list(TableParser.sectionsFromTableDump("oasisDump.txt"));


#print([sec.name for sec in allSections if sec.getLectureByDay(SectionHandle.Day.SUN) is not None]);

filtered = Analysis.filterIterable(allSections, Analysis.genFilterAtDayAndTime(SectionHandle.Day.MON, datetime.time(10,15)))

print(Analysis.reduceDict(Analysis.accumulatePopulation, filtered, 0, Analysis.getBuilding));