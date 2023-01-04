import datetime

import click

from ritmo.models import models
from ritmo.session import session


@click.command(name="add", help="Add a new habit.")
@click.option(
    "--name",
    "-n",
    prompt="Habit name",
    prompt_required=True,
    help="Name of the habit.",
    required=True,
)
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
def add_habit(
    name: str,
    description: str,
    type: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
):
    """
    Add a new habit to the tracking system.
    """

    if end_date and start_date and end_date < start_date:
        click.echo("End date must be after start date.")
        return

    Session = session.create_session("sqlite:///habit.db")
    with Session.begin() as sess:
        sess.add(models.Habit(name=name, description=description, type=type))
        sess.commit()


@click.command(name="list", help="List habits.")
def list_habits():
    """
    List all habits.
    """

    Session = session.create_session("sqlite:///habit.db")
    with Session.begin() as sess:
        habits = sess.query(models.Habit).all()
        for habit in habits:
            click.echo(
                f"Name: {habit.name}, Description: {habit.description}, "
                f"Type: {habit.type}, Start date: {habit.start_date}, "
                f"End date: {habit.end_date}"
            )


@click.command(name="update", help="Update an existing habit.")
@click.option(
    "--name",
    "-n",
    prompt="Habit name",
    prompt_required=True,
    help="Name of the habit.",
    required=True,
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
def update_habit(
    name: str,
    description: str,
    type: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
):
    """
    Update a habit.
    """

    if end_date and start_date and end_date < start_date:
        click.echo("End date must be after start date.")
        return

    Session = session.create_session("sqlite:///habit.db")
    with Session.begin() as sess:
        habit = sess.query(models.Habit).filter(models.Habit.name == name).first()
        if habit:
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


@click.command(name="delete", help="Delete a habit.")
@click.option(
    "--name",
    "-n",
    prompt="Habit name",
    prompt_required=True,
    help="Name of the habit.",
    required=True,
)
def delete_habit(name: str):
    """
    Delete a habit.
    """

    Session = session.create_session("sqlite:///habit.db")
    with Session.begin() as sess:
        habit = sess.query(models.Habit).filter(models.Habit.name == name).first()

        if habit:
            sess.delete(habit)
            sess.commit()
        else:
            click.echo(f"Habit '{name}' not found.")
