from googleapiclient.discovery import build
from lesson import Lesson
from enums import DateType
from controllers.dateTimeController import DateController
from controllers.googleApiController import GoogleApiController
import requests
import re
from bs4 import BeautifulSoup
from LessonsTable import LessonsTable


class MainController():
  instance = None
  def __init__(self, group: str):
    if (MainController.instance != None): return MainController.instance
    MainController.instance = self

    self.dateController = DateController()
    self.calendarController = GoogleApiController(self.dateController)

    link = MainController.getSheetLink()

    self.lessonsTable = LessonsTable(link, group)
    self.group = group
    
  def loadLessonsFromSheet(self):
    self.lessonsTable.load()
    self.lessons = self.lessonsTable.getLessons()

  def loadLessonsToCalendar(self):
    self.calendarController.createCalendar(self.group)  
    
    for lesson in self.lessons:
      self.calendarController.addEvent(lesson)
    
    self.calendarController.transferCalendarToUserAccount()

  def loadAndSendCalendar(self):
    self.loadLessonsFromSheet()
    self.loadLessonsToCalendar()

  def getSheetLink ():
    url = "https://kpfu.ru/computing-technology/raspisanie"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    for strong in soup.findAll('strong'):
      if strong.parent.name == 'a' and re.search('Расписание на', strong.text):
        return (strong.parent["href"])
