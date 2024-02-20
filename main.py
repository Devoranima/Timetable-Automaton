from timetableController import MainController


def Handler(group: str):
  TimetableController = MainController(group)
  TimetableController.loadAndSendCalendar()


def main():
  group = "09-111 (2)"
  Handler(group)

    
if __name__ == "__main__":
  main()