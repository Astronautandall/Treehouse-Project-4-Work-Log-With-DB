import datetime

import utils
from models import Task
from models import Employee


class TaskSearch():

    def search_by_date(self):
        """ Search a task by date"""

        date = utils.create_date('Enter the date')

        # Format the date to dd/mm/yyyy
        date = utils.format_date(date)
        rows = (
            Task.select(Task, Employee)
            .join(Employee)
            .where(Task.date == date)
            .naive()
        )

        return rows

    def search_by_dates_range(self):
        """Search task between range of dates"""

        date1 = utils.create_date('Start date')
        date2 = utils.create_date('Finish date')

        if date1 < date2:
            start_date = date1
            finish_date = date2
        elif date1 > date2:
            start_date = date2
            finish_date = date1

        # Format dates
        start_date = utils.format_date(start_date)
        finish_date = utils.format_date(finish_date)

        rows = (
            Task.select(Task, Employee)
            .join(Employee)
            .where(Task.date.between(start_date, finish_date))
            .naive()
        )

        return rows

    def search_by_term(self):

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
            term = utils.get_input('Enter your term here: ')

            if not term:
                utils.pause('Error: Blank spaces are not allowed')
                continue
            else:
                break

        rows = (
            Task.select(Task, Employee)
            .join(Employee)
            .where(Task.title.contains(term) | Task.notes.contains(term))
            .naive()
        )

        return rows

    def search_by_regex(self):

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
            regex = utils.get_input('Enter your regex here: ')

            if not regex:
                utils.pause('Error: Blank spaces are not allowed')
                continue
            else:
                break

        rows = (
            Task.select(Task, Employee)
            .join(Employee)
            .where(Task.title.regexp(regex))
            .naive()
        )

        return rows

    def search_by_employee(self):

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
            name = utils.get_input('Enter the name of the Employee: ')

            if not name:
                utils.pause('Error: Blank spaces are not allowed')
                continue
            else:
                break

        employees = Employee.select().where(Employee.name.contains(name))

        # Creating a list for get the
        employees_list = []

        # And another to display a selecting menu
        employees_menu = []

        if len(employees) > 1:
            counter = 1

            for employee in employees:
                employees_list.append(employee)
                employees_menu.append("{}) {}".format(counter, employee.name))
                counter += 1

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
            print("Select one Employee: \n" + "\n".join(employees_menu))
            option = utils.parse_int(utils.get_input('>'))

            if option:
                if option not in range(len(employees) + 1) and option != 0:
                    utils.pause("Error: {} isn't a valid option")
                    continue
            else:
                utils.pause("Error: {} is not a number")
                continue

            try:
                employee = employees_list[option - 1]
            except IndexError:
                continue

            break

        tasks = (
            Task.select(Employee.name)
            .join(Employee)
            .where(Task.id_employee == employee.id_employee)
            .naive()
        )

        return tasks
