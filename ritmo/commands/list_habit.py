import click
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from ritmo.decorators import with_sqlalchemy_error_handling
from ritmo.models import Habit
from ritmo.sessions import create_local_session


def list_habit(sess: Session) -> None:
    """
    List all habits.

    Args:
        sess: The database session.
    """

    table = Table(show_header=True, title="Habits")
    table.add_column("Name")
    table.add_column("Description")
    table.add_column("Type")
    table.add_column("Start date")
    table.add_column("End date")

    habits = sess.query(Habit).all()
    for habit in habits:
        table.add_row(
            habit.name,
            habit.description if habit.description else "None",
            habit.type,
            habit.start_date.strftime("%Y-%m-%d"),
            habit.end_date.strftime("%Y-%m-%d") if habit.end_date else "None",
        )

    console = Console()
    console.print(table)


@click.command(name="list", help="List habits.")
@with_sqlalchemy_error_handling
def list_habit_cmd(description: bool, start_date: bool, end_date: bool):
    local_session = create_local_session()
    with local_session.begin() as sess:
        list_habit(sess)
