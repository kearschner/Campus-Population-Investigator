import CampusPop.SectionHandle as SectionHandle
import CampusPop.TableParser as TableParser
import CampusPop.Analysis as Analysis
import datetime
import matplotlib.pyplot as plt

allSections : list[SectionHandle.Section] = list(TableParser.sectionsFromTableDump("oasisDump.txt"));


#print([sec.name for sec in allSections if sec.getLectureByDay(SectionHandle.Day.SUN) is not None]);

#plt.plot(list(Analysis.popAcrossDay(allSections, SectionHandle.Day.MON, 15)))
#plt.plot(list(Analysis.popAcrossDay(allSections, SectionHandle.Day.TUE, 15)))
#plt.plot(list(Analysis.popAcrossDay(allSections, SectionHandle.Day.WED, 15)))
#plt.plot(list(Analysis.popAcrossDay(allSections, SectionHandle.Day.THU, 15)))
#plt.plot(list(Analysis.popAcrossDay(allSections, SectionHandle.Day.FRI, 15)))

#plt.show()

#filtered = Analysis.filterIterable(allSections, Analysis.genFilterAtDayAndTime(SectionHandle.Day.MON, datetime.time(12,15)))
#print(Analysis.reduceDict(Analysis.accumulatePopulation, filtered, 0, Analysis.getBuilding));