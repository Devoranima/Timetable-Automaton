from calendarAutomaton.timetableController import CalendarController, DateController
from lesson import Lesson
from enums import Weekday

controller = CalendarController("80e33c4faec073828dbd4e61d96e5edee99477df0ed2230a30f6c9ba980a10bc@group.calendar.google.com"
)
dummy = Lesson('8.30-10.00', Weekday.MONDAY, False, "(2-5 неделя) Безопасность жизнедеятельности. Хабибрахманов И.И.  ауд.  КЗВК (Кремл.18)")

#controller.addEvent(dummy)
#controller.deleteCalendar("80e33c4faec073828dbd4e61d96e5edee99477df0ed2230a30f6c9ba980a10bc@group.calendar.google.com"
#)