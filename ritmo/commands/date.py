import datetime

import click
from rich.console import Console
from rich.table import Table

from ritmo.decorators import decorators
from ritmo.models import models


@click.command(name="date", help="Show habit status for a specific date.")
@click.argument(
    "date",
    nargs=1,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=datetime.datetime.now(),
)
@decorators.with_database
@decorators.with_sqlalchemy_error_handling
def show_date(sess, date: datetime.datetime):
    """
    Show habit status for a specific date.

    Args:
        sess: The database session.
        date: The date to show the habit status for (defaults to today).
    """

    habits = sess.query(models.Habit).all()
    habit_day = sess.query(models.HabitDay).filter_by(date=date.date())

    if habit_day.count() == 0:
        click.echo(f"No habits status for {date.date()}")
        return

    table = Table(show_header=True, title=f"{date.date()}")
    table.add_column("Name")
    table.add_column("Completed")

    for habit in habits:
        day_record = habit_day.filter_by(habit_id=habit.id).first()

        if day_record is None:
            table.add_row(habit.name, "No")
        else:
            if habit.type == "numerical":
                times_done = day_record.completed_num
                if times_done == 1:
                    table.add_row(habit.name, f"{times_done} time")
                else:
                    table.add_row(habit.name, f"{times_done} times")
            else:
                table.add_row(habit.name, "Yes")

    console = Console()
    console.print(table)


@click.command(name="today", help="Show today's habit status.")
@decorators.with_database
@decorators.with_sqlalchemy_error_handling
def show_today(sess):
    """
    Show today's habit status.

    Args:
        sess: The database session.
    """

    show_date(sess)
