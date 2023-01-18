import datetime

import click
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from ritmo.decorators import with_sqlalchemy_error_handling
from ritmo.models import Habit, HabitLog
from ritmo.sessions import create_local_session


def get_by_date(sess: Session, date: datetime.datetime) -> None:
    """
    Get habit logs for a specific date.

    Args:
        sess: The database session.
        date: The date to show the habit logs for (defaults to today).
    """

    habits = sess.query(Habit).all()
    if len(habits) == 0:
        click.echo("No habits to show.")
        return

    table = Table(show_header=True, title=f"{date.date()}")
    table.add_column("Name")
    table.add_column("Completed")

    for habit in habits:
        habit_logs = (
            sess.query(HabitLog)
            .filter(HabitLog.habit_id == habit.id, HabitLog.date == date.date())
            .all()
        )

        if len(habit_logs) == 0:
            table.add_row(habit.name, "No")
        else:
            if habit.type == "boolean":
                table.add_row(habit.name, "Yes")
            else:
                table.add_row(habit.name, f"{len(habit_logs)} times")

    console = Console()
    console.print(table)


@click.command(name="date", help="Show habit logs for a specific date.")
@click.argument(
    "date",
    nargs=1,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=datetime.datetime.utcnow().strftime("%Y-%m-%d"),
)
@with_sqlalchemy_error_handling
def show_date_cmd(date: datetime.datetime) -> None:
    local_session = create_local_session()
    with local_session.begin() as sess:
        get_by_date(sess, date)


@click.command(name="today", help="Show today's habit log.")
@with_sqlalchemy_error_handling
def show_today_cmd() -> None:
    """
    Show today's habit logs.
    """

    local_session = create_local_session()
    with local_session.begin() as sess:
        get_by_date(sess, datetime.datetime.utcnow())


@click.command(name="yesterday", help="Show yesterday's habit logs.")
@with_sqlalchemy_error_handling
def show_yesterday_cmd() -> None:
    """
    Show yesterday's habit logs.
    """

    yesterday_date = datetime.datetime.now() - datetime.timedelta(days=1)
    local_session = create_local_session()
    with local_session.begin() as sess:
        get_by_date(sess, yesterday_date)
