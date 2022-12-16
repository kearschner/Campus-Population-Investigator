from lxml import etree, html
import typing
import CampusPop.SectionHandle as SectionHandle
import CampusPop.CellHandle as CellHandle

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
							CellHandle.isPermitLocked(row[8]),
							CellHandle.convertTermDates(row[9]),
							CellHandle.convertDays(row[10]),
							CellHandle.convertTimeFrame(row[11]),
							int(row[12]),
							int(row[13]),
							row[16],
							row[17],
							CellHandle.convertLocation(row[18]),
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
						CellHandle.convertTermDates(row[9]),
						CellHandle.convertDays(row[10]),
						CellHandle.convertTimeFrame(row[11]),
						row[16],
						row[17],
						CellHandle.convertLocation(row[18]),
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