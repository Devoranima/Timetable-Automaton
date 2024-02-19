from enums import Weekday, DateType

class Lesson():
  previousInterval = None
  def __init__(self, time: str, day: Weekday, elective: bool = False, raw: str = None):
    self.weekday = day
    self.time = time.strip()
    self.raw = raw
    self.elective = elective
    if raw: self.prepare()

  def prepare(self):
    words = [x.strip() for x in self.raw.split(' ') if x.strip() != '']
    i = 0

    if (words[i].startswith('н/н')):
      self.dateType = DateType.ODD
    elif (words[i].startswith('ч/н')):
      self.dateType = DateType.EVEN
    else:
      self.dateType = DateType.COMMON
      i-=1
    i+=1

    self.dateInterval = ""
  
  
    if (words[i].startswith('(')):
      while (words[i].endswith(')') == False):
        self.dateInterval += words[i] + ' '
        i+=1
      self.dateInterval += words[i]
      i+=1
      Lesson.previousInterval = self.dateInterval
    else:
      self.dateInterval = Lesson.previousInterval


    self.name = ""
    while (words[i].endswith('.') == False):
      self.name += words[i] + ' '
      i+=1
    self.name += words[i]
    i+=1

    self.teacher = words[i] + ' ' + words[i+1]
    i+=2

    self.auditorium = ""
    while i < len(words):
      self.auditorium += words[i] + ' '
      i+=1


      
  def __str__(self):
    if (self.raw):
      return "\t{0}: {1} {2} {3}".format(self.time, self.name, self.auditorium, self.auditorium)
    else:
      return "\t{0}: ~~~~~~~".format(self.time)