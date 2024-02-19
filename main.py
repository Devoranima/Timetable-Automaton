import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
from sheet import LessonsTable
from enums import GroupByMode
import json
from calendarController import CalendarController

__numberOfLessonsPerDay__ = 7
__numberOfDays__ = 6

def getSheetLink ():
  url = "https://kpfu.ru/computing-technology/raspisanie"
  page = requests.get(url)
  soup = BeautifulSoup(page.text, "html.parser")

  for strong in soup.findAll('strong'):
    if strong.parent.name == 'a' and re.search('Расписание на', strong.text):
      return (strong.parent["href"])

def main():
  link = getSheetLink()
  group = "09-111 (2)"

  lessonsTable = LessonsTable(link, group)
  controller = CalendarController()

  lessons = lessonsTable.getLessons()
  for lesson in lessons:
    controller.addEvent(lesson)
    
if __name__ == "__main__":
  main()