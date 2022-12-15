import CampusPop.SectionHandle as SectionHandle
import CampusPop.TableParser as TableParser
import datetime

allSections : list[SectionHandle.Section] = list(TableParser.sectionsFromTableDump("oasisDump.txt"));

for sec in allSections:
	print("%s" % sec);

#print([sec.name for sec in allSections if sec.getLectureByDay(SectionHandle.Day.SUN) is not None]);

filtered = SectionHandle.filterIterable(allSections, SectionHandle.genFilterAtDayAndTime(SectionHandle.Day.SUN, datetime.time(8,15)))

print(SectionHandle.countPopOfSections(filtered))