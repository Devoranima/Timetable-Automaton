from calendarController import CalendarController, DateController
from lesson import Lesson
from enums import Weekday

controller = CalendarController()
dummy = Lesson('8.30-10.00', Weekday.MONDAY, False, "(2-5 неделя) Безопасность жизнедеятельности. Хабибрахманов И.И.  ауд.  КЗВК (Кремл.18)")

controller.addEvent(dummy)