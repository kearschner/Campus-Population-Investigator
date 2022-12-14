from io import StringIO
from lxml import etree

oasisFile = open("oasisDump.txt", "r");

htmlTable : str = oasisFile.read();

parser = etree.HTMLParser();
tree = etree.parse(StringIO(htmlTable), parser);

result = etree.tostring(tree.getroot(), pretty_print=True, method="html");

print(result);
