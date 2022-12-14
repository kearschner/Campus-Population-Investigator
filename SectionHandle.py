import enum

class Section:


	def __init__(self) -> None:
		pass;

class Location():

    def __init__(self, locStr : str) -> None:
        self.building, self.room = locStr.split(' ');

    def __str__(self) -> str:
        return "%s %s" % (self.building, self.room);


class Day(enum.Flag):
    MON = enum.auto();
    TUE = enum.auto();
    WED = enum.auto();
    THU = enum.auto();
    FRI = enum.auto();
    SAT = enum.auto();
    SUN = enum.auto();

    @staticmethod
    def fromString(dayString : str) -> "Day":
        if dayString == "M":
            return Day.MON;
        if dayString == "T":
            return Day.TUE;
        if dayString == "W":
            return Day.WED;
        if dayString == "R":
            return Day.THU;
        if dayString == "F":
            return Day.FRI;
        if dayString == "S":
            return Day.SAT;
        if dayString == "U":
            return Day.SUN;

        return Day(0);