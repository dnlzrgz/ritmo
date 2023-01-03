import datetime

import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ritmo.models.models import Base, Habit

Session = sessionmaker()
engine = create_engine("sqlite:///habits.db")
Base.metadata.create_all(engine)


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--name",
    prompt="Habit name",
    prompt_required=True,
    help="Name of the habit.",
    required=True,
)
@click.option(
    "--description",
    prompt="Habit description",
    prompt_required=False,
    help="Description of the habit.",
)
@click.option(
    "--type",
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
def add(
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

    Session.configure(bind=engine)
    with Session.begin() as sess:
        sess.add(Habit(name=name, description=description, type=type))
        sess.commit()


@click.command()
def list():
    """
    List all habits.
    """

    Session.configure(bind=engine)
    with Session.begin() as sess:
        habits = sess.query(Habit).all()
        for habit in habits:
            click.echo(
                f"Name: {habit.name}, Description: {habit.description}, "
                f"Type: {habit.type}, Start date: {habit.start_date}, "
                f"End date: {habit.end_date}"
            )


@cli.command()
@click.option(
    "--name",
    prompt="Habit name",
    prompt_required=True,
    help="Name of the habit.",
    required=True,
)
@click.option(
    "--description",
    prompt="Habit description",
    prompt_required=False,
    help="Description of the habit",
)
@click.option(
    "--type",
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
def update(
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

    Session.configure(bind=engine)
    with Session.begin() as sess:
        habit = sess.query(Habit).filter(Habit.name == name).first()
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


@click.command()
@click.option(
    "--name",
    prompt="Habit name",
    prompt_required=True,
    help="Name of the habit.",
    required=True,
)
def delete(name: str):
    """
    Delete a habit.
    """

    Session.configure(bind=engine)
    with Session.begin() as sess:
        habit = sess.query(Habit).filter(Habit.name == name).first()

        if habit:
            sess.delete(habit)
            sess.commit()
        else:
            click.echo(f"Habit '{name}' not found.")


cli.add_command(add)
cli.add_command(list)
cli.add_command(update)
cli.add_command(delete)


def run():
    cli()


if __name__ == "__main__":
    run()
