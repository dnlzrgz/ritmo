import click

from ritmo.commands import (
    add_habit_cmd,
    delete_habit_cmd,
    list_habit_cmd,
    mark_as_done_cmd,
    mark_as_undone_cmd,
    show_date_cmd,
    show_today_cmd,
    show_yesterday_cmd,
    update_habit_cmd,
)


@click.group()
def cli():
    pass


cli.add_command(add_habit_cmd)
cli.add_command(list_habit_cmd)
cli.add_command(update_habit_cmd)
cli.add_command(delete_habit_cmd)
cli.add_command(mark_as_done_cmd)
cli.add_command(mark_as_undone_cmd)
cli.add_command(show_date_cmd)
cli.add_command(show_today_cmd)
cli.add_command(show_yesterday_cmd)


def run():
    cli()


if __name__ == "__main__":
    run()
