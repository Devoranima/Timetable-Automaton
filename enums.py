from enum import Enum

class DateType(Enum):
  COMMON = 0
  ODD = 1
  EVEN = 2

class Weekday(Enum):
  MONDAY = 1
  TUESDAY = 2
  WEDNESDAY = 3
  THURSDAY = 4
  FRIDAY = 5
  SATURDAY = 6
  SUNDAY = 7

class GroupByMode(Enum):
  WEEKDAY = 0