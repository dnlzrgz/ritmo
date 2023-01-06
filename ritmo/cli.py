import click

from ritmo.commands.crud import add_habit, delete_habit, list_habits, update_habit
from ritmo.commands.date import show_date, show_today
from ritmo.commands.manage import mark_done, mark_undone


@click.group()
def cli():
    pass


cli.add_command(add_habit)
cli.add_command(list_habits)
cli.add_command(update_habit)
cli.add_command(delete_habit)
cli.add_command(mark_done)
cli.add_command(mark_undone)
cli.add_command(show_date)
cli.add_command(show_today)


def run():
    cli()


if __name__ == "__main__":
    run()
