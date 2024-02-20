import datetime
from enums import DateType
from lesson import Lesson

class DateController():
  def __init__(self):
    self.start = datetime.datetime.strptime('02/05/24', '%m/%d/%y').date()
    self.updateTimeDate()

  def updateTimeDate(self):
    self.today = datetime.datetime.now().date()
    self.weekNum = ((self.today - self.start).days)//7 + 1
    self.evenWeekStartDate =  self.start + datetime.timedelta(
      weeks=(self.weekNum - (1 if self.weekNum % 2 == 0 else 0))
    )
    self.oddWeekStartDate =  self.start + datetime.timedelta(
      weeks=(self.weekNum - (1 if self.weekNum % 2 == 1 else 0))
    )
    self.currentWeekStartDate = self.start + datetime.timedelta(
      weeks=(self.weekNum - 1)
    )
  
  def getLessonDateTimeString(self, lesson:Lesson):
    [start, end] = lesson.time.split('-')
    start = datetime.datetime.strptime(start, '%H.%M').time()
    end = datetime.datetime.strptime(end, '%H.%M').time()

    weekStart = self.currentWeekStartDate
    if lesson.dateType == DateType.EVEN:
      weekStart = self.evenWeekStartDate
    elif lesson.dateType == DateType.ODD:
      weekStart = self.oddWeekStartDate

    day = weekStart + datetime.timedelta(days=(lesson.weekday.value - 1))

    startDate = datetime.datetime.combine(day, start)
    endDate = datetime.datetime.combine(day, end)
    return [startDate.strftime('%Y-%m-%dT%H:%M:%S+03:00'), endDate.strftime('%Y-%m-%dT%H:%M:%S+03:00')]