import datetime
from typing import Optional

import click
from sqlalchemy.orm import Session

from ritmo.decorators import with_sqlalchemy_error_handling
from ritmo.models import Habit
from ritmo.sessions import create_local_session


def add_habit(
    sess: Session,
    name: str,
    description: Optional[str | None],
    type: Optional[str | None],
    start_date: Optional[datetime.datetime | None],
    end_date: Optional[datetime.datetime | None],
) -> None:
    """
    Add a new habit to the database.

    Args:
        sess: The database session.
        name: The name of the habit.
        description: A description of the habit.
        type: The type of tracking system to use.
        start_date: The date the habit starts.
        end_date: The date the habit ends.
    """

    if end_date and start_date and end_date < start_date:
        click.echo("End date must be after start date.")
        return

    if not name or name.isspace():
        click.echo("Habit name must be specified.")
        return

    habit = sess.query(Habit).filter(Habit.name == name).first()

    if habit:
        return
    else:
        sess.add(Habit(name=name, description=description, type=type))
        sess.commit()


@click.command(name="add", help="Add a new habit.")
@click.argument("name", nargs=1, type=str, required=True)
@click.option(
    "--description",
    "-d",
    prompt="Habit description",
    prompt_required=False,
    help="Description of the habit.",
)
@click.option(
    "--type",
    "-t",
    prompt="Type of tracking system",
    prompt_required=False,
    default="boolean",
    type=click.Choice(["boolean", "numerical"], case_sensitive=False),
    help="Type of tracking system.",
)
@click.option(
    "--start-date",
    prompt="Start date",
    prompt_required=False,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Start date in 'Y-m-d' format.",
)
@click.option(
    "--end-date",
    prompt="End date",
    prompt_required=False,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="End date in 'Y-m-d' format.",
)
@with_sqlalchemy_error_handling
def add_habit_cmd(
    name: str,
    description: str,
    type: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
) -> None:
    local_session = create_local_session()
    with local_session.begin() as sess:
        add_habit(sess, name, description, type, start_date, end_date)
