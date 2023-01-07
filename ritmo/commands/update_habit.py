import datetime

import click
from sqlalchemy.orm import Session

from ritmo.decorators import with_sqlalchemy_error_handling
from ritmo.models import Habit
from ritmo.sessions import create_local_session


def update_habit(
    sess: Session,
    name: str,
    new_name: str,
    description: str,
    type: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
):
    """
    Update an existing habit.

    Args:
        sess: The database session.
        name: The name of the habit.
        new_name: The new name of the habit.
        description: A description of the habit.
        type: The type of tracking system to use.
        start_date: The date the habit starts.
        end_date: The date the habit ends.
    """

    if not name:
        click.echo("Habit name must be provided.")
        return

    if end_date and start_date and end_date < start_date:
        click.echo("End date must be after start date.")
        return

    habit = sess.query(Habit).filter(Habit.name == name).first()
    if habit:
        if new_name:
            habit.name = new_name
        if description:
            habit.description = description
        if type:
            habit.type = type
        if start_date:
            habit.start_date = start_date
        if end_date:
            habit.end_date = end_date
        sess.commit()
    else:
        click.echo(f"Habit '{name}' not found.")


@click.command(name="update", help="Update an existing habit.")
@click.argument("name", nargs=1, type=str)
@click.option(
    "--new-name",
    "-n",
    prompt="Habit name",
    prompt_required=False,
    help="Name of the habit.",
)
@click.option(
    "--description",
    "-d",
    prompt="Habit description",
    prompt_required=False,
    help="Description of the habit",
)
@click.option(
    "--type",
    "-t",
    prompt="Type of tracking system",
    prompt_required=False,
    default="boolean",
    type=click.Choice(["boolean", "numerical"], case_sensitive=False),
    help="Type of tracking system",
)
@click.option(
    "--start-date",
    prompt="Start date",
    prompt_required=False,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Start date in UTC format",
)
@click.option(
    "--end-date",
    prompt="End date",
    prompt_required=False,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="End date in UTC format",
)
@with_sqlalchemy_error_handling
def update_habit_cmd(
    name: str,
    new_name: str,
    description: str,
    type: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
):
    local_session = create_local_session()
    with local_session.begin() as sess:
        update_habit(sess, name, new_name, description, type, start_date, end_date)
