from googleapiclient.discovery import build
from google.oauth2 import service_account
import googleapiclient
from lesson import Lesson
from enums import DateType
from controllers.dateTimeController import DateController

class GoogleApiController():
  def __init__(self, dateController: DateController):
    credentials = service_account.Credentials.from_service_account_file("C:\\PythonProjects\\calendarAutomaton\\token.json", scopes=['https://www.googleapis.com/auth/calendar'])
    self.service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    
    self.dateController = dateController
    
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
      "recurrence": ["RRULE:FREQ=WEEKLY;INTERVAL={0};UNTIL=20240528".format(1 if lesson.dateType == DateType.COMMON else 2)],
      'colorId': '9' if lesson.elective else '10' 
    }

    event = self.service.events().insert(calendarId=self.calendarId, body=event).execute()

  def createCalendar(self, name):
    new_calendar = {
      'summary': name,
      'timeZone': 'Europe/Moscow'
    }
    created_calendar = self.service.calendars().insert(body=new_calendar).execute()
    self.calendarId = created_calendar['id']
    
  def getAllCalendars(self):
    page_token = None
    while True:
      calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
      for calendar_list_entry in calendar_list['items']:
        print (calendar_list_entry['summary'])
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break

  def clearAllCalendars(self):
    page_token = None
    while True:
      calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
      for calendar_list_entry in calendar_list['items']:
        self.service.calendars().delete(calendarId=calendar_list_entry['id']).execute()
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break

  def transferCalendarToUserAccount(self):
    rule = {
      'scope': {
        'type': 'user',
        #! transfer to .env
        'value': 'ali3v5t1limaw@gmail.com'
      },
      'role': 'owner'
    }
    self.service.acl().insert(calendarId=self.calendarId, body=rule).execute()