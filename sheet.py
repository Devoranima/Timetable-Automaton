import pandas as pd
import re
from lesson import Lesson
from enums import Weekday, GroupByMode

__numberOfLessonsPerDay__ = 7
__numberOfDays__ = 6



class LessonsTable():

  def __init__(self, link: str, group: str):
    self.link = link
    self.raw = pd.read_excel(link)
    self.group = group
    self.loadTimetable()
    self.loadLessons()

  def __getGroupLessonsColumn__(self):
    groupStart = self.group[:5] + "1 (1)"
    groupEnd = self.group[:5] + "3 (2)"

    columnStart = int(self.raw.where(self.raw==groupStart).dropna(how='all').dropna(axis=1).columns[0][-2:])
    columnEnd = int(self.raw.where(self.raw==groupEnd).dropna(how='all').dropna(axis=1).columns[0][-2:])
    columnNumber = int(self.raw.where(self.raw==self.group).dropna(how='all').dropna(axis=1).columns[0][-2:])

    offset = (int(self.group[-5:-4])-1)*2
    frame = self.raw.iloc[:, columnStart:columnEnd+1].ffill(axis=1)
    frame = frame.iloc[:, offset:offset+2].ffill(axis=1)

    return frame.iloc[:, columnNumber - columnStart - offset]


  def loadTimetable(self):
    self.__timetable__ = self.raw.iloc[:, 0:2].ffill(axis=0)
  
  def loadLessons(self):
    lessons = []
    lessonsFrame = self.__getGroupLessonsColumn__()

    def handleFrameValue(value: str):
      elective = re.search("Дисциплины по выбору:", value)
      if (elective):
        value = re.sub("Дисциплины по выбору: ", '', value)

      for lesson in value.split(';'):
        #! ну какого хуя в расписании лежит одиночный блядь перенос занятия
        if (lesson.strip().startswith('занятие')): continue
        lessons.append(Lesson(time[base+k], Weekday(i+1), elective, lesson))

    time = self.__timetable__.iloc[:, 1]

    base = 16
    shift = __numberOfLessonsPerDay__*2+1
    for i in range(__numberOfDays__):
      for j in range(__numberOfLessonsPerDay__*2):
        k = i * shift + j
        value = lessonsFrame.iloc[base + k]

        if (type(value) == float):
          if (j%2 == 0):
            lessons.append(Lesson(time[base+k], Weekday(i+1)))
            j+=1
        else:
          handleFrameValue(value)
        
        #! А че бля, думал в кфу нормально расписание составляют? Нет 64 строки ебать, пошел нахуй, пидор
        if (base + k == 62):
          base+=1
    self.__lessons__ = lessons

  def getLessons(self):
    return self.__lessons__
  
  def groupBy(self, mode: GroupByMode):
    if (mode == GroupByMode.WEEKDAY):
      result = {}
      for day in Weekday:
        filteredLessons = list(filter(lambda s: s.weekday == day, self.__lessons__))
        if len(filteredLessons) > 0:
          result[day.name] = filteredLessons
      return result
    else: 
      return self.__lessons__