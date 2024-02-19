import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import googleapiclient
from lesson import Lesson
from enums import DateType


SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


class CalendarController():
  calendarId = "80e33c4faec073828dbd4e61d96e5edee99477df0ed2230a30f6c9ba980a10bc@group.calendar.google.com"
  def __init__(self):
    credentials = service_account.Credentials.from_service_account_file("C:\\PythonProjects\\calendarAutomaton\\token.json")
    self.service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    self.dateController = DateController()

  def addEvent(self, lesson: Lesson):
    if not lesson.raw: return False

    [start, end] = self.dateController.getLessonDateTimeString(lesson)
    event = {
      'summary': lesson.name,
      'location': lesson.auditorium,
      'description': lesson.teacher,
      'start': {
        'dateTime': start,
        'timeZone': 'Europe/Moscow',
      },
      'end': {
        'dateTime': end,
        'timeZone': 'Europe/Moscow',
      },
      #TODO: change to dynamic interval
      "recurrence": ["RRULE:FREQ=WEEKLY;INTERVAL={0};UNTIL=20240528".format(1 if lesson.dateType == DateType.COMMON else 2)],
      'colorId': '9' if lesson.elective else '10' 
    }

    event = self.service.events().insert(calendarId=self.calendarId, body=event).execute()
    

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