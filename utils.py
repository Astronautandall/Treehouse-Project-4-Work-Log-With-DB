from datetime import datetime

DATEFORMAT = '%d/%m/%Y'


def cls():
    """Clean the screen"""

    print("\033c", end="")
    return True


def get_input(text=''):
    """Returns an input"""

    return input(text).strip()


def pause(msg='', inputtext='Press ENTER to  try again'):
    """Create a pause for the program"""

    print(msg)
    get_input(inputtext)


def format_date_input(date):
    """Create a datetime from an input data"""
    return datetime.strptime(date, DATEFORMAT)


def format_date(date):
    """Format a date from a datetime object"""

    return date.strftime(DATEFORMAT)


def parse_int(string):
    """Parse a string to an int"""

    try:
        parsed_str = int(string)
    except ValueError:
        return False
    else:
        return parsed_str


def create_date(msg=None):
    """ Prompts the user to give a date and validates it """

    while True:

        cls()
        print(msg)
        date_input = get_input('Please use DD/MM/YYYY: ')

        try:
            date = format_date_input(date_input)
        except ValueError:
            pause("Error: {} isn't a valid date".format(date_input))
            continue
            raise
        else:
            return date
