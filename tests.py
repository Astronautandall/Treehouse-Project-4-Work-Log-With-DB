import unittest
from unittest.mock import patch
import datetime

import models
import utils
import task
import tasksearch
import worklog

DATETIME_CONST = datetime.datetime(2017, 8, 14, 0, 0)
DATETIME_CONST2 = datetime.datetime(2017, 8, 2, 0, 0)


class Models(unittest.TestCase):

    def test_initialize(self):
        self.assertTrue(models.initialize())


class TaskTest(unittest.TestCase):

    @patch('task.Task.ask_employee', return_value=1)
    @patch('task.Task.ask_date', return_value='14/08/2017')
    @patch('task.Task.ask_title', return_value='Aloha')
    @patch('task.Task.ask_time_spent', return_value=10)
    @patch('task.Task.ask_notes', return_value='Notas')
    def setUp(self, mock1, mock2, mock3, mock4, mock5):
        self.task = task.Task(True)

    @patch('task.Task.ask_employee', return_value=1)
    @patch('task.Task.ask_date', return_value='14/08/2017')
    @patch('task.Task.ask_title', return_value='Aloha')
    @patch('task.Task.ask_time_spent', return_value=10)
    @patch('task.Task.ask_notes', return_value='Notas')
    def test_get(self, mock1, mock2, mock3, mock4, mock5):
        self.assertEqual(self.task.get(), task.Task(True).get())

    @patch('utils.create_date', return_value=DATETIME_CONST)
    def test_ask_date(self, mock_create_date):
        self.assertEqual(self.task.date, self.task.ask_date())

    @patch('utils.get_input', return_value='Task Title')
    def test_ask_title(self, mock_get_input):
        self.assertEqual(self.task.ask_title(), 'Task Title')

    @patch('utils.get_input', return_value='Notes')
    def test_ask_notes(self, mock_get_input):
        self.assertEqual(self.task.ask_notes(), 'Notes')

    @patch('utils.get_input', return_value='3')
    def test_ask_time_spent(self, mock1):
        self.assertEqual(self.task.ask_time_spent(), 3)

    @patch('utils.cls', return_value=None)
    @patch('utils.get_input', return_value="")
    def test_ask_employee(self, mock1, mock2):
        self.task.ask_employee()


class UtilsTest(unittest.TestCase):

    def test_format_date_input(self):
        self.assertEqual(utils.format_date_input('14/08/2017'), DATETIME_CONST)

    def test_format_date(self):
        self.assertEqual(utils.format_date(DATETIME_CONST), '14/08/2017')

    @patch('utils.get_input')
    def test_get_input(self, mock_get_input):
        mock_get_input.return_value = 'aloha'
        self.assertEqual(utils.get_input(), 'aloha')

    @patch('utils.get_input', return_value='14/08/2017')
    def test_get_date(self, mock_get_input):
        date = datetime.datetime(2017, 8, 14, 0, 0)
        self.assertEqual(utils.create_date(), date)


class WorkLogTest(unittest.TestCase):

    def setUp(self):
        self.worklog = worklog.WorkLog()

    @patch('worklog.WorkLog.menu', return_value=None)
    def test_main(self, mock1):
        worklog.main()

    @patch('utils.get_input', return_value="")
    @patch('utils.pause', return_value=None)
    def test_display_results_empty(self, mock1, mock2):

        models.initialize()
        rows = (
            models.Task.select(models.Task, models.Employee)
            .join(models.Employee)
            .naive()
        )
        self.worklog.display_results(rows)

    @patch('utils.get_input', return_value="s")
    @patch('utils.pause', return_value=None)
    def test_display_results_wrong(self, mock1, mock2):

        models.initialize()
        rows = (
            models.Task.select(models.Task, models.Employee)
            .join(models.Employee)
            .naive()
        )
        self.worklog.display_results(rows)

    @patch('utils.cls', return_value=None)
    @patch('utils.pause', return_value=None)
    @patch('utils.get_input', return_value="")
    def test_patch_empty(self, mock1, mock2, mock3):
        self.worklog.patch(None)

    @patch('utils.cls', return_value=None)
    @patch('utils.pause', return_value=None)
    @patch('utils.get_input', return_value="invalid")
    def test_patch_wrong(self, mock1, mock2, mock3):
        self.worklog.patch(None)

    @patch('utils.pause', return_value=None)
    @patch('utils.get_input', return_value="a")
    @patch('utils.create_date', return_value=DATETIME_CONST)
    def test_patch_date(self, mock1, mock2, mock3):
        models.initialize()
        task = models.Task.get()
        self.worklog.patch(task)

    @patch('utils.cls', return_value=None)
    @patch('utils.pause', return_value=None)
    @patch('utils.get_input', return_value="b")
    @patch('task.Task.ask_title', return_value='A')
    def test_patch_title(self, mock1, mock2, mock3, mock4):
        models.initialize()
        task = models.Task.get()
        self.worklog.patch(task)

    @patch('utils.cls', return_value=None)
    @patch('utils.pause', return_value=None)
    @patch('utils.get_input', return_value="c")
    @patch('task.Task.ask_time_spent', return_value=1)
    def test_patch_time_spent(self, mock1, mock2, mock3, mock4):
        models.initialize()
        task = models.Task.get()
        self.worklog.patch(task)

    @patch('utils.cls', return_value=None)
    @patch('utils.pause', return_value=None)
    @patch('utils.get_input', return_value="")
    def test_delete_empty(self, mock1, mock2, mock3):
        self.worklog.delete(None)

    @patch('utils.cls', return_value=None)
    @patch('utils.pause', return_value=None)
    @patch('utils.get_input', return_value="x")
    def test_delete_wrong(self, mock1, mock2, mock3):
        self.worklog.delete(None)

    @patch('utils.cls', return_value=None)
    @patch('utils.pause', return_value=None)
    @patch('utils.get_input', return_value="n")
    def test_delete(self, mock1, mock2, mock3):
        self.worklog.delete(None)

    @patch('utils.cls', return_value=None)
    @patch('utils.get_input', return_value='')
    @patch('utils.pause', return_value=None)
    def test_menu_empty(self, mock1, mock2, mock3):
        self.worklog.menu()

    @patch('utils.cls', return_value=None)
    @patch('utils.get_input', return_value='a')
    @patch('utils.pause', return_value=None)
    @patch('worklog.WorkLog.put', return_value=None)
    def test_menu_option_a(self, mock1, mock2, mock3, mock4):
        self.worklog.menu()

    @patch('utils.cls', return_value=None)
    @patch('utils.get_input', return_value='b')
    @patch('utils.pause', return_value=None)
    @patch('worklog.WorkLog.search', return_value=None)
    def test_menu_option_b(self, mock1, mock2, mock3, mock4):
        self.worklog.menu()

    @patch('utils.get_input', return_value='c')
    @patch('utils.pause', return_value=None)
    @patch('sys.exit', return_value=None)
    def test_menu_option_a(self, mock1, mock2, mock3):
        self.worklog.menu()

    @patch('utils.cls', return_value=None)
    @patch('utils.get_input', return_value='invalid')
    @patch('utils.pause', return_value=None)
    def test_search_whole(self, mock1, mock2, mock3):
        self.worklog.search()

    @patch('utils.cls', return_value=None)
    @patch('utils.get_input', return_value='')
    @patch('utils.pause', return_value=None)
    def test_search_no_option(self, mock1, mock2, mock3):
        self.worklog.search()

    @patch('utils.cls', return_value=None)
    @patch('utils.get_input', return_value="a")
    @patch('utils.pause', return_value=None)
    @patch('tasksearch.TaskSearch.search_by_date', return_value='')
    def test_search_exact_date(self, mock1, mock2, mock3, mock4):
        self.worklog.search()

    @patch('utils.cls', return_value=None)
    @patch('utils.get_input', return_value="b")
    @patch('utils.pause', return_value=None)
    @patch('tasksearch.TaskSearch.search_by_dates_range', return_value='')
    def test_search_by_dates_range(self, mock1, mock2, mock3, mock4):
        self.worklog.search()

    @patch('utils.cls', return_value=None)
    @patch('utils.get_input', return_value="c")
    @patch('utils.pause', return_value=None)
    @patch('tasksearch.TaskSearch.search_by_term', return_value='')
    def test_search_by_term(self, mock1, mock2, mock3, mock4):
        self.worklog.search()

    @patch('utils.cls', return_value=None)
    @patch('utils.get_input', return_value="d")
    @patch('utils.pause', return_value=None)
    @patch('tasksearch.TaskSearch.search_by_regex', return_value='')
    def test_search_by_regex(self, mock1, mock2, mock3, mock4):
        self.worklog.search()

    @patch('utils.cls', return_value=None)
    @patch('utils.get_input', return_value="e")
    @patch('utils.pause', return_value=None)
    @patch('tasksearch.TaskSearch.search_by_employee', return_value='')
    def test_search_by_employee(self, mock1, mock2, mock3, mock4):
        self.worklog.search()

    @patch('utils.cls', return_value=None)
    @patch('utils.get_input', return_value="f")
    @patch('utils.pause', return_value=None)
    @patch('worklog.WorkLog.menu', return_value=None)
    def test_search_menu_exit(self, mock1, mock2, mock3, mock4):
        self.worklog.search()

    @patch('utils.cls', return_value=None)
    def test_patch(self, mock1):
        pass


class TaskSearchTest(unittest.TestCase):

    def setUp(self):
        self.tasksearch = tasksearch.TaskSearch()

    @patch('utils.create_date', return_value=DATETIME_CONST)
    def test_search_by_date(self, mock1):
        self.tasksearch.search_by_date()

    @patch('utils.create_date', side_effect=[DATETIME_CONST, DATETIME_CONST2])
    def test_search_by_dates_range(self, mock1):
        self.tasksearch.search_by_dates_range()

    @patch('utils.create_date', side_effect=[DATETIME_CONST2, DATETIME_CONST])
    def test_search_by_dates_range2(self, mock1):
        self.tasksearch.search_by_dates_range()

    @patch('utils.cls', return_value=None)
    @patch('utils.get_input', return_value="")
    def test_search_by_term_empty_term(self, mock1, mock2):
        self.tasksearch.search_by_term()

    @patch('utils.cls', return_value=None)
    @patch('utils.get_input', return_value="term")
    def test_search_by_term(self, mock1, mock2):
        self.tasksearch.search_by_term()

    @patch('utils.cls', return_value=None)
    @patch('utils.get_input', return_value="")
    @patch('utils.pause', return_value=None)
    def test_search_by_regex_empty_regex(self, mock1, mock2, mock3):
        self.tasksearch.search_by_regex()

    @patch('utils.cls', return_value=None)
    @patch('utils.get_input', return_value="regex")
    @patch('utils.pause', return_value=None)
    def test_search_by_regex(self, mock1, mock2, mock3):
        self.tasksearch.search_by_regex()

    @patch('utils.cls', return_value=None)
    @patch('utils.pause', return_value=None)
    @patch('utils.get_input', return_value="")
    def test_search_by_employee_empty_employee(self, mock1, mock2, mock3):
        self.tasksearch.search_by_employee()

    @patch('utils.cls', return_value=None)
    @patch('utils.pause', return_value=None)
    @patch('utils.get_input', side_effect=["Bryan", "1"])
    def test_search_by_employee(self, mock1, mock2, mock3):

        self.tasksearch.search_by_employee()


if __name__ == '__main__':
        unittest.main()
