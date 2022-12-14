from lxml import etree
import typing
import SectionHandle

def getPrimativeRow(rowElement : etree._Element) -> list[str]:
	assert rowElement.tag == "tr"
	return [etree.tostring(elem, encoding="unicode", method="text")[:-1] for elem in rowElement.iterchildren(tag="td")];

def tBodyFromRoot(root : etree._Element) -> etree._Element:
	return root[0][0][1];

def yieldSections(rows : typing.Iterator[list[str]]) -> typing.Generator[SectionHandle.Section]:
	pass

oasisFile = open("oasisDump.txt", "r");

htmlTable : str = oasisFile.read();

parser : etree.HTMLParser = etree.HTMLParser();
root : etree._Element = etree.fromstring(htmlTable,  parser);

tableBody : etree._Element = tBodyFromRoot(root);

cellGenerator : typing.Iterator[list[str]] = ((getPrimativeRow(elem)) for elem in tableBody.iterchildren(tag="tr"));
for cell in cellGenerator:
	print(cell);