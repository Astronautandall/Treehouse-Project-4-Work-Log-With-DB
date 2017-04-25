import sys

from datetime import datetime
from task import Task
from tasksearch import TaskSearch

import utils
import models


class WorkLog():

    def __init__(self):

        models.initialize()
        self.task_table = models.Task()

    def menu(self):

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

            menu = (
                "WORK LOG\n"
                "What do you want to do? \n"
                "a) Add new entry \n"
                "b) Search in existing entries \n"
                "c) Quit program \n"
                ">"
            )

            option = utils.get_input(menu).lower()

            # Handling the errors first
            if not option:
                utils.pause('Error: Blank spaces are not allowed')
                continue
            elif option not in 'abc':
                utils.pause("Error: {} isn't a valid option".format(option))
                continue

            # If nothing wrong, then go ahead with the options
            if option == 'a':
                self.put()
            elif option == 'b':
                self.search()
                break
            elif option == 'c':
                utils.cls()
                print('Au revoir!')
                sys.exit()

    def put(self):
        """ Add a row to the Task Table"""

        # Create the task and then call the get function
        # to have the data in a dict and add it to the db
        task = Task(True).get()

        # The dict needs to be unpacked
        self.task_table.create(**task)

        utils.cls()
        input('The entry hass been add. Press enter to return to the menu')

    def search(self):
        """ Search a task """

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

            menu = (
                    "Do you want to search by: \n"
                    "a) Exact Date \n"
                    "b) Range of Dates \n"
                    "c) Term \n"
                    "d) Regex Pattern \n"
                    "e) Employee \n"
                    "f) Return to menu \n"
                    ">"
            )

            option = utils.get_input(menu).lower()

            # Handling the errors first
            if not option:
                utils.pause('Error: Blank spaces are not allowed')
                continue
            elif option not in 'abcdef':
                utils.pause("Error: {} isn't a valid option".format(option))
                continue

            tasksearch = TaskSearch()

            if option == 'a':
                rows = tasksearch.search_by_date()
            elif option == 'b':
                rows = tasksearch.search_by_dates_range()
            elif option == 'c':
                rows = tasksearch.search_by_term()
            elif option == 'd':
                rows = tasksearch.search_by_regex()
            elif option == 'e':
                rows = tasksearch.search_by_employee()
            else:
                # Get us back to the initial menu
                return self.menu()

            self.display_results(rows)

    def display_results(self, rows):

        # Checking if there is any data
        if not rows:
            utils.pause('Ops! Nothing found', 'Press ENTER to continue')
            return False

        # Counter for the loop
        current = 0
        # Counting how many results there are to display it to the user
        no_results = len(rows)

        task_list = []

        for result in rows:

            task_list.append(result)

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

            task = task_list[current]
            print("Employee: {}\nDate: {}\nTitle: {}\nTime Spent: {}\nNote: {}"
                  .format(task.name, task.date, task.title,
                          task.time_spent, task.notes))
            print('\nResult {} of {}\n'.format(current + 1, no_results))

            # Checking if it is not the first element
            if current != 0:
                print('[P]revious, ', end='')

            # Checking if it is not the last element
            if current < no_results - 1:
                print('[N]ext, ', end='')

            # Printing the other options
            print('[E]dit, [D]elete, [F]inish')
            option = utils.get_input().lower()

            # Handling errors first
            if not option:
                utils.pause('Error: Blank spaces are not allowed')
                continue
            elif option not in 'pnedf':
                utils.pause('Error: {} is not a valid option'.format(option))
                continue

            if option == 'p':
                current -= 1
            elif option == 'n':
                current += 1
            elif option == 'e':
                self.patch(task)
            elif option == 'd':
                self.delete(task)
            elif option == 'f':
                break

    def patch(self, task):

        task_obj = Task()

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

            menu = (
                    "What do you want to edit of the task?: \n"
                    "a) Date \n"
                    "b) Title \n"
                    "c) Time Spent \n"
                    "d) Notes \n"
                    "e) Save changes and return to searches \n"
                    "f) Return to menu \n"
                    ">"
            )

            option = utils.get_input(menu)

            # Handling errors
            if not option:
                utils.pause('Error: Blank spaces are not allowed')
                continue
            elif option not in 'abcdef':
                utils.pause('Error: {} is not a valid option'.format(option))
                continue

            # Task Date
            if option == 'a':

                utils.cls()
                print('Current task date: {}'.format(task.date))
                new_task_date = utils.create_date('New Date: ')

                task.date = new_task_date.strftime(utils.DATEFORMAT)

            # Task Title
            elif option == 'b':

                utils.cls()
                current = 'Current task name: {}'.format(task.title)
                task.title = task_obj.ask_title(current + '\nNew title: ')

            # Task Time Spent
            elif option == 'c':

                utils.cls()
                current = 'Current task time spent: {}'.format(task.time_spent)
                task.time_spent = task_obj.ask_time_spent(
                    current + '\nNew time spent (rounded minutes): ')

            # Task Notes
            elif option == 'd':

                utils.cls()
                print('Actual Notes: {}'.format(task.notes))
                new_task_notes = input('New Notes (Optional can be empty): ')

                task.notes = new_task_notes

            # Save changes and commit them
            elif option == 'e':

                task.save()

                utils.cls()
                print('Nice, changes saved')
                input('Press ENTER to continue')
                return self.menu()

            # Return to initial menu
            elif option == 'f':
                break

    def delete(self, task):

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
            confirm = utils.get_input('Are you sure? [y/n]').strip()

            # Handling errors
            if not confirm:
                utils.pause('Error: Blank spaces are not allowed')
                continue
            elif confirm not in 'yn':
                utils.pause("Error: {} isn't a valid option".format(confirm))
                continue
            else:
                break

        # If the user changes of idea, getting them back to the
        # main menu
        if confirm == 'y':
            task.delete_instance()
            utils.cls()
            utils.pause('Task deleted!', 'Press ENTER to continue')
            return self.menu()
        else:
            utils.cls()
            utils.pause('The task is safe!', 'Press ENTER to continue')
            return self.menu()


def main():

    work_log = WorkLog()
    work_log.menu()


# Make sure the script doesn't execute when imported
# All of the logic and function should be called in
# __name__ == "__main__": block.
if __name__ == '__main__':

    main()
