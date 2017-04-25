from datetime import datetime

import utils
from models import Employee


class Task:

    def __init__(self, init=False):

        if init:
            self.id_employee = self.ask_employee(
                'Complete name of the employee: ')
            self.date = self.ask_date('Date of the task: ')
            self.title = self.ask_title('Title of the task: ')
            self.time_spent = self.ask_time_spent(
                'Time spent (rounded minutes): ')
            self.notes = self.ask_notes(
                'Notes (Optional, you can leave this empty): ')

    def get(self):
        """Return the data of the task as a dict"""

        data = {
            'id_employee': self.id_employee,
            'date': self.date,
            'title': self.title,
            'time_spent': self.time_spent,
            'notes': self.notes
        }

        return data

    def ask_employee(self, inputtxt=None):
        """Ask the title for the task"""

        while_breaker = 1

        while True:

            # This helps the testing, since these are kind of
            # infinite loops while testing, there's need for something
            # that can break them automatically
            if while_breaker > 100:
                break
            else:
                while_breaker += 1

            utils.cls()
            name = utils.get_input(inputtxt)

            if not name:
                utils.pause('Error: Blanks spaces are not allowed')
                continue

            try:
                employee = Employee.get(Employee.name == name)
            except Employee.DoesNotExist:
                employee = Employee.create(name=name)

            return employee.id_employee

    def ask_date(self, inputtxt=None):
        """Ask the date for the task"""

        date = utils.create_date(inputtxt)
        return utils.format_date(date)

    def ask_title(self, inputtxt=None):
        """Ask the title for the task"""

        while True:

            utils.cls()
            title = utils.get_input(inputtxt)

            if not title:
                utils.pause('Error: Blanks spaces are not allowed')
                continue

            return title

    def ask_time_spent(self, inputtxt=None):
        """Ask the time spent for the task"""

        while True:

            utils.cls()
            timespent_input = utils.get_input(inputtxt)

            if not timespent_input:
                utils.pause('Error: Blank spaces are not allowed')
                continue

            try:
                time_spent = int(timespent_input)
            except ValueError:
                utils.pause("Error: {} isn't a whole number"
                            .format(timespent_input))
                continue
            else:
                return time_spent

    def ask_notes(self, inputtxt=None):
        """Ask the notes for the task (optionals)"""

        utils.cls()
        notes = utils.get_input(inputtxt)
        return notes
