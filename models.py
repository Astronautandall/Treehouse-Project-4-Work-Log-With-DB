from peewee import *


db = SqliteDatabase('tasks.db')


class Employee(Model):
    id_employee = PrimaryKeyField()
    name = CharField(max_length=255)

    class Meta:
        database = db


class Task(Model):
    id_task = PrimaryKeyField()
    id_employee = ForeignKeyField(Employee, to_field="id_employee")
    date = DateField()
    title = CharField(max_length=255)
    time_spent = IntegerField()
    notes = TextField(null=True)

    class Meta:
        database = db


def initialize():
    """Initalize the dabatase."""

    # Connecting to the database
    db.get_conn()
    # Creating the tables if they don't exist
    db.create_tables([Employee, Task], safe=True)

    return True
