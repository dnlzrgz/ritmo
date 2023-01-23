import click
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from ritmo.decorators import with_sqlalchemy_error_handling
from ritmo.models import Habit
from ritmo.sessions import create_local_session


def list_habit(sess: Session, sort_by: str, reverse: bool) -> None:
    """
    List all habits.

    Args:
        sess: The database session.
        sort_by: Sorting criteria
        reverse: Reverse sorting criteria
    """

    table = Table(show_header=True, title="Habits")
    table.add_column("Name")
    table.add_column("Description")
    table.add_column("Type")
    table.add_column("Start date")
    table.add_column("End date")

    habits = sess.query(Habit).all()
    if len(habits) == 0:
        click.echo("No habits found")
        return

    if sort_by == "name":
        habits.sort(key=lambda habit: habit.name, reverse=reverse)
    elif sort_by == "start-date":
        print("sorting by date")
        habits.sort(key=lambda habit: habit.start_date, reverse=reverse)
    elif sort_by == "end-date":
        habits.sort(
            key=lambda habit: (habit.end_date is None, habit.end_date), reverse=reverse
        )

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
@click.option(
    "--sort-by",
    type=click.Choice(["name", "start-date", "end-date"], case_sensitive=True),
    help="Sorting criteria",
    default="name",
    show_default=True,
)
@click.option(
    "--reverse",
    is_flag=True,
    help="Reverse sorting criteria",
    default=False,
    show_default=True,
)
@with_sqlalchemy_error_handling
def list_habit_cmd(sort_by: str, reverse: bool):
    local_session = create_local_session()
    with local_session.begin() as sess:
        list_habit(sess, sort_by, reverse)
