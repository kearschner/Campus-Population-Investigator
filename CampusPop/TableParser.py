from lxml import etree, html
import typing
import functools
import datetime

import CampusPop.SectionHandle as SectionHandle


@functools.cache
def convertDays(daysString : str) -> SectionHandle.Day:
    days = SectionHandle.Day(0);

    for day in daysString:
        days |= SectionHandle.Day.fromString(day);

    return days;


@functools.lru_cache(maxsize=24)
def hourMap(num : int, afternoon : bool) -> int:
    if not afternoon:
        return num % 12;
    
    if num == 12:
        return 12;
    
    return num + 12;


def convertTime(timeString : str) -> typing.Optional[datetime.time]:

    if "N/A" in timeString:
        return None;

    if "TBA" in timeString:
        return None;

    afternoon : bool = 'pm' in timeString;
    
    hour = hourMap(int(timeString[:2]), afternoon);
    
    return datetime.time(hour, int(timeString[3:5]));


def convertDate(timeString : str) -> datetime.date:
    return datetime.date(2001, int(timeString[:2]), int(timeString[-2:]));


T = typing.TypeVar('T')
def convertRange(operation : typing.Callable[[str], typing.Optional[SectionHandle.SelfComparable]], sep : str) -> typing.Callable[[str], typing.Optional[SectionHandle.Range]]:

    def conversionFunc(input : str) -> typing.Optional[SectionHandle.Range]:
        if sep not in input:
            return None;
        endPoints : list[str] = input.split(sep);
        start = operation(endPoints[0]);
        end = operation(endPoints[1]);

        if start is None or end is None:
            return None;
        return SectionHandle.Range(start, end);

    return conversionFunc;


convertTimeFrame = functools.cache(convertRange(convertTime, '-'));

convertTermDates = functools.cache(convertRange(convertDate, '-'));


def convertLocation(locString : str) -> typing.Optional[SectionHandle.Location]:

    if "TBA" in locString:
        return None;

    return SectionHandle.Location(locString);


def convertSeats(capString : str, availString : str) -> int:
    return int(capString) - int(availString);


def isPermitLocked(permString : str) -> bool:
    return 'Y' == permString; 


def getPrimativeRow(rowElement : etree._Element) -> list[str]:
	assert rowElement.tag == "tr"
	return [etree.tostring(elem, encoding="unicode", method="text")[:-1] for elem in rowElement.iterchildren(tag="td")];


def isNewSection(row : list[str], sec : SectionHandle.Section) -> bool:
	return row[1] != '\xa0' and row[1] != sec.crn;


def firstRowSection(row : list[str]) -> SectionHandle.Section:
	return SectionHandle.Section(
							row[1],
							SectionHandle.Course(row[2], row[3]),
							row[4],
							row[5],
							row[6],
							SectionHandle.InstructionalMethod.fromString(row[7]),
							isPermitLocked(row[8]),
							convertTermDates(row[9]),
							convertDays(row[10]),
							convertTimeFrame(row[11]),
							int(row[12]),
							int(row[13]),
							row[16],
							row[17],
							convertLocation(row[18]),
							row[19]);
											

def yieldSections(rows : typing.Iterator[list[str]]) -> typing.Iterator[SectionHandle.Section]:
	
	currSect = None;

	for row in rows:

		if len(row) != 20:
			continue;
		
		if currSect is None or isNewSection(row, currSect):
			currSect = firstRowSection(row);
			yield currSect;
			continue;

		if not isNewSection(row, currSect):
			currSect = currSect.copyForNewDay(
						convertTermDates(row[9]),
						convertDays(row[10]),
						convertTimeFrame(row[11]),
						row[16],
						row[17],
						convertLocation(row[18]),
						row[19]);
			yield currSect;
			continue;
		

def sectionsFromTableDump(filePath : str) -> typing.Iterator[SectionHandle.Section]:

	oasisFile = open(filePath, "r");

	htmlTable : str = oasisFile.read();

	parser : etree.HTMLParser = etree.HTMLParser();
	root : etree._Element = html.fromstring(htmlTable, parser=parser);

	tableBody : etree._Element = root[1];

	return yieldSections(((getPrimativeRow(elem)) for elem in tableBody.iterchildren(tag="tr")));


if __name__ == "__main__":
	for sec in sectionsFromTableDump("oasisDump.txt"):
		print(sec);